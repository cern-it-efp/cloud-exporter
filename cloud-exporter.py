#!/usr/bin/env python

import sys
import os
import requests
import yaml
import json
import shutil

def checkProperties(configs):
    if configs['title'] == None or configs['title'] == "":
        print("'title' is a required property")
        sys.exit(2)
    if configs['title'].strip() == None or configs['title'].strip() == "":
        print("'title' property missing or badly formatted")
        sys.exit(2)
    if configs['path_to_data'] == None or configs['path_to_data'] == "":
        print("'path_to_data' is a required property")
        sys.exit(2)
    if configs['access_token'] == None or configs['access_token'] == "":
        print("'access_token' is a required property")
        sys.exit(2)

def init_checks():
    global configs
    global base_url
    global filename
    global access_token
    if os.path.exists("configs.yaml") == False:
        print("Configuration file not found")
        sys.exit(2)
    with open("configs.yaml", 'r') as stream:
        try:
            configs = yaml.load(stream)
        except yaml.YAMLError as exc:
            print("Error loading configs.yaml file")
            sys.exit(2)
    checkProperties(configs)
    if configs['path_to_data'][-1:] == '/': configs['path_to_data'] = configs['path_to_data'][:-1]
    if os.path.exists(configs['path_to_data']) == False:
        print("No such file or directory "+configs['path_to_data'])
        sys.exit(2)
    base_url = "https://sandbox.zenodo.org" if configs['sandbox'] == True else "https://zenodo.org"
    filename = configs['path_to_data'].split('/')[::-1][0]
    access_token = configs['access_token']
    if filename == "":
        print("property 'path_to_data' is wrong!")
        sys.exit(2)

def checkResponse(r):
    succeed = [200,201,202,204]
    if r.status_code not in succeed:
        print(json.dumps(r.json()))
        sys.exit(2)

init_checks()

print("===========================================================================")
print(" Starting to upload '"+filename+"' to "+base_url+"...")
print("===========================================================================")

if os.path.isdir(configs['path_to_data']) == True:
    print("Compressing directory to upload...")
    shutil.make_archive(filename, 'zip', configs['path_to_data'])
    filename = filename+".zip"

print("Creating upload...")
headers = {"Content-Type": "application/json"}
r = requests.post(base_url+"/api/deposit/depositions", params={'access_token': access_token}, json={}, headers=headers)
checkResponse(r)

print("Uploading file...")
deposition_id = r.json()['id']
data = {'filename': filename}
r = requests.post(base_url+'/api/deposit/depositions/%s/files' % deposition_id, params={'access_token': access_token}, data=data, files={'file': open(filename, 'rb')})
checkResponse(r)

print("Adding metadata...")
metadata = {
    'metadata': {
        'title':configs['title'],
        'upload_type':'other',
        'description':'Uploaded using cloud-exporter'
        }
}
r = requests.put(base_url+'/api/deposit/depositions/%s' % deposition_id, params={'access_token': access_token}, data=json.dumps(metadata), headers=headers)
checkResponse(r)

print("===========================================================================")
print(" Successfully uploaded '"+filename+"' to "+base_url)
print("===========================================================================")
