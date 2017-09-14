import googleapiclient.discovery
from jinja2 import Environment, FileSystemLoader
import json
import os
import requests
import sys
import sh

token = os.getenv('TOKEN')
project = os.getenv('PROJECT')

def list_rules():
    compute = googleapiclient.discovery.build('compute', 'v1')
    result = compute.firewalls().list(project=project).execute()
    return result['items']

# for i in list_rules():
#     print(i['name'])

if len(sys.argv) > 1:
    if str(sys.argv[1]) == 'state':
        for i in list_rules():
            rule = "google_compute_firewall.{}".format(i['name'])
            sh.terraform("import", rule, i['name'])
    elif str(sys.argv[1]) == 'config':
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('firewall.j2')
        output_from_parsed_template = template.render(rules=list_rules())
        print output_from_parsed_template
    else:
        raise ValueError('you need to specify to either generate config or state')
else:
    raise ValueError('you need to specify to either generate config or state')
