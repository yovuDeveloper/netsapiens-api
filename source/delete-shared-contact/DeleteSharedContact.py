# YOVU Office Phones - Netsapiens API - Delete Netsapiens Shared Contact
# Developed by YOVU Development Team
# Author : Vishnu Anilkumar 22/09/2020

import csv
import requests
import json
import logging
import datetime
import configparser
import os
import time

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

base_url = 'https://{}'.format(server)

#Authentication
def get_token():
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
        logging.debug('OAuth Failed')
        return ''

def create_header():
    token = get_token()
    bearer = "Bearer {}".format(token)
    header = {'Authorization': bearer}
    return header

#Get a list of shared contacts for the domain
def get_shared_contacts():
    shared_contact_url = base_url+'/ns-api/?format=json&object=contact&action=read&user=domain&domain='+domain
    header = create_header()
    response = requests.post(shared_contact_url,headers=header)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logging.debug('Failed to get list of Users in Domain- {}'.format(domain))

#Second validation to make sure all contacts are shared
def validate_shared_contact(list_of_shared):
    validated_list = []
    for contact in list_of_shared:
        if 'shared' in contact:
            if contact['shared']:
                validated_list.append(contact)
    return validated_list

#Delete contact from list
def delete_contact_from_list(list_to_delete):
    f1 = open('success.csv', 'w',newline='')
    c1 = csv.writer(f1)
    f2 = open('fail.csv', 'w',newline='')
    c2 = csv.writer(f2)
    header = create_header()
    count = 0
    for contact in list_to_delete:
        if 'contact_id' in contact:
            count +=1
            shared_contact_url = base_url+'/ns-api/?object=contact&action=delete&contact_id='+contact['contact_id']
            response = requests.post(shared_contact_url,headers=header)
            if count % 25 == 0:
                time.sleep(5)
                if response.status_code == 202:
                    c1.writerow(contact.values())
                else:
                    c2.writerow(contact.values())
    
    print('Completed')
    logging.debug('Task Completed')



    
    



list_of_shared = get_shared_contacts() 
validated_list = validate_shared_contact(list_of_shared) 
delete_contact_from_list(validated_list)