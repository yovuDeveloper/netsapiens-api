# YOVU Office Phones - Netsapiens API - Delete Netsapiens Shared Contact
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
import tkinter as tk

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

base_url = 'https://{}'.format(server)

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
def get_shared_contacts():
    shared_contact_url = base_url+'/ns-api/?format=json&object=contact&action=read&user=domain&domain='+domain
    header = create_header()
    response = requests.post(shared_contact_url,headers=header)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        global res
        res = 'Failed to get list of Users in Domain- {}'.format(domain)
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
            if response.status_code == 202:
                c1.writerow(contact.values())
            else:
                c2.writerow(contact.values())
    
    print('Completed.')
    global res
    res = 'Task Completed'
    logging.debug('Task Completed')



    
    

window = tk.Tk()
window.title("YOVU Netsapiens API")
window.geometry('640x480')
greeting = tk.Label(window,text="Netsapiens API",font=("Arial Bold", 13))
greeting.pack()
##Server
server_label = tk.Label(window,text="Server")
server_input = tk.Entry(width=30)
server_input.insert(0,server)
server_label.pack()
server_input.pack()
##Domain Name
domain_name_label = tk.Label(window,text="Domain Name")
domain_name_input = tk.Entry(width=30)
domain_name_input.insert(0,domain)
domain_name_label.pack()
domain_name_input.pack()
##Client Id
client_id_label = tk.Label(window,text="Client Id")
client_id_input = tk.Entry(width=50)
client_id_input.insert(0,client_id)
client_id_label.pack()
client_id_input.pack()
##Client Secret
client_secret_label = tk.Label(window,text="Client Secret")
client_secret_input = tk.Entry(window,show="*",width=50)
client_secret_input.insert(0,client_secret)
client_secret_label.pack()
client_secret_input.pack()

##Username
username_label = tk.Label(window,text="Username")
username_input = tk.Entry(width=50)
username_input.insert(0,username)
username_label.pack()
username_input.pack()

##Password
password_label = tk.Label(window,text="Password")
password_input = tk.Entry(window,show="*",width=50)
password_input.insert(0,password)
password_label.pack()
password_input.pack()

##Output
op_label = tk.Label(window,text='Hello',font=("Arial Bold", 21))
op_label.pack()

#clicked function
def clicked():
    button.configure(state="disable")
    op_label.configure(text='In Progress')
    global server
    global client_id
    global client_secret
    global username
    global password
    global domain
    server= server_input.get()
    client_id= client_id_input.get()
    client_secret= client_secret_input.get()
    username= username_input.get()
    password = password_input.get()
    domain = domain_name_input.get()
    list_of_shared = get_shared_contacts() 
    if list_of_shared is None:
        global res
        res = 'No shared contact found.'
    else:    
        validated_list = validate_shared_contact(list_of_shared) 
        delete_contact_from_list(validated_list)
    op_label.configure(text=res+' Please review NSlog.log for more details')
    button.configure(state="normal")

#button.grid(column=1, row=0)
button = tk.Button(window,text="Delete all Shared Contacts",command=clicked)
button.pack()
window.mainloop()



#list_of_shared = get_shared_contacts() 
#validated_list = validate_shared_contact(list_of_shared) 
#delete_contact_from_list(validated_list)