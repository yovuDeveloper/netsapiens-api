# Scripts using Netsapiens API
## 1. Delete all Shared Contacts
```source/delete-shared-contact/DeleteSharedContact.py```


You can delete all shared contacts using this script. You may repurpose the script to loop through your own list of contact ids and delete them from the server.

>__Warning__: 
Make sure you know what you are doing before proceeding. Backup if needed. We are not responsible for any changes you make to your system using this script.
### __Files__
You must add your credentails in ```Settings.ini``` for the script to work.These details are used for Authentication
1. Server Name. example: api.netsapiens.com ; Please do not include http// or https://
1. API Client Id : Client Id of your app that you created in Netsapiens.
1. Client Secret : Client Secret corresponding to the client id above.
1. Domain : Domain Name from which you want to delete the shared contacts.
1. User Name : Your login username for the server.
1. Password :  Your password you use to login.

__After Execution of the script:__ 

Logs can be found in : ```NSLog.log```  
```Success.csv``` will hold the list of shared contacts that were successfully deleted.  
```Fail.csv``` will hold the list of shared contacts that were not deleted.


*__Technical Details__:
There is a 5 second delay after every 25th delete request in case you are deleting a lot of request. But it is recommended to batchify the code if required.* 



