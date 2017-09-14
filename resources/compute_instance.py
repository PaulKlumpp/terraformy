import googleapiclient.discovery
from jinja2 import Environment, FileSystemLoader
import json
import os
import requests
import sys


token = os.getenv('TOKEN')
project = os.getenv('PROJECT')
zone = os.getenv('ZONE')


def list_instances():
    compute = googleapiclient.discovery.build('compute', 'v1')
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']


def get_info(url):
    headers = {
            'Authorization': 'Bearer {}'.format(token),
    }
    r = requests.get(url, headers=headers)
    return json.loads(r.content)


def get_boot_disk_info(disks):
    for idx, d in enumerate(disks):
        if d['boot'] is True:
            disk = get_info(d['source'])
            return {'source_image': disk['sourceImage'].rsplit('/', 1)[-1],
                    'type': disk['type'].rsplit('/', 1)[-1],
                    'size': disk['sizeGb'],
                    'index': idx,
                    'existing': (True if 'lastDetachTimestamp' in disk else False),
                    'name': disk['name'],
                    }


def get_other_disks(disks, boot_disk_idx):
    attached_disks = list(disks)
    del attached_disks[boot_disk_idx]
    return attached_disks


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
template.globals['get_boot_disk_info'] = get_boot_disk_info
template.globals['get_other_disks'] = get_other_disks
output_from_parsed_template = template.render(instances=list_instances())
print output_from_parsed_template
