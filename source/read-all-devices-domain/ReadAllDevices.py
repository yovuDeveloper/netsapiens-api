# YOVU Office Phones - Read all Devices/Subscribers in a Domain
# Developed by YOVU Development Team

import csv
import requests
import json
import logging
import datetime
import configparser
import os
import time
import sys

LOG_FILENAME = 'NSLog.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.debug('Log Created at {}'.format(datetime.datetime.now()))
file_path = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(file_path, 'Settings.ini')
config = configparser.ConfigParser()
config.read(config_file)
server= config['CREDS']['server']
client_id= config['CREDS']['client_id']
client_secret= config['CREDS']['client_secret']
username= config['CREDS']['username']
password = config['CREDS']['password']
domain = config['CREDS']['domain']
res=''
header=''

base_url = 'https://{}'.format(server)
device_list=[]
class Device:
    aor=''
    mac=''
    model=''
    user_agent=''
    mode=''
    subscriber_name=''
    sub_fullname='' 
    domain_name='' 
    def __iter__(self):
        return iter([self.aor,self.mac,self.model,self.user_agent,self.mode,self.subscriber_name,self.sub_fullname,self.domain_name])

#Authentication
def get_token():
    print(password)
    payload = {'client_id':client_id,'client_secret':client_secret,'username':username,'password':password}
    oauth_url = base_url+'/ns-api/oauth2/token/?grant_type=password'
    response = requests.get(oauth_url ,params=payload)
    logging.debug(response.status_code)
    if response.status_code == 200:
        logging.debug('oAuth Successful')
        data=response.json()
        token = data["access_token"]
        logging.debug(token)
        return token
    else:
        global res
        res = 'Authentication Failed'
        logging.debug('OAuth Failed')
        return ''

def create_header():
    token = get_token()
    bearer = "Bearer {}".format(token)
    header = {'Authorization': bearer}
    return header

#Get a list of shared contacts for the domain
def read_all_devices(domainName):
    read_all_devices_url = base_url+'/ns-api/?format=json&object=device&action=read&domain='+domainName
    print(header)
    global device_list
    print(domainName)
    response = requests.post(read_all_devices_url,headers=header)
    if response.status_code == 200:
        data = response.json()
        for i in data:
            if 'mac' in i:
                device = Device()
                device.aor = i['aor']
                device.mac = i['mac']
                device.model = i['model']
                device.user_agent = i['user_agent']
                device.mode = i['mode']
                device.subscriber_name = i['subscriber_name']
                device.sub_fullname = i['sub_fullname']
                device.domain_name = domainName
                print(device.aor)
                device_list.append(device)

       
    else:
        global res
        res = 'Failed to get list of Users in Domain- {}'.format(domainName)
        logging.debug('Failed to get list of Users in Domain- {}'.format(domainName))


def create_final_csv():
    final_list = open('ListOfSubscribers.csv','w',newline='')
    final_list_writer = csv.writer(final_list)
    for obj in device_list:
        print(list(obj))
        final_list_writer.writerow(list(obj))

#get_domain_list()
header = create_header()
read_all_devices('domainName')
create_final_csv()

