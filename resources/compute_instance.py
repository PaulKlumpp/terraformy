import googleapiclient.discovery
from jinja2 import Environment, FileSystemLoader
import json
import os
import requests
import sys


token = os.getenv('TOKEN')
project = os.getenv('PROJECT')

def list_instances():
    compute = googleapiclient.discovery.build('compute', 'v1')
    result = compute.instances().list(project=project, zone='europe-west1-b').execute()
    return result['items']

def get_info(url):
    headers = {
            'Authorization': 'Bearer {}'.format(token),
    }
    r = requests.get(url, headers=headers)
    return json.loads(r.content)

def get_disk_info(url):
    disk = get_info(url)
    return {'source_image': disk['sourceImage'].rsplit('/', 1)[-1],
            'type': disk['type'].rsplit('/', 1)[-1],
            'size': disk['sizeGb'],
            }
# print(get_disk_info(''))
# for i in list_instances():
#     print(i)

env = Environment(loader=FileSystemLoader('templates'))
if len(sys.argv) > 1:
    if str(sys.argv[1]) == 'state':
        template = env.get_template('compute_instance.tfstate.j2')
    elif str(sys.argv[1]) == 'config':
        template = env.get_template('compute_instance.j2')
    else:
        raise ValueError('you need to specify to either generate config or state')
else:
    raise ValueError('you need to specify to either generate config or state')
template.globals['get_disk_info'] = get_disk_info
output_from_parsed_template = template.render(instances=list_instances())
print output_from_parsed_template
