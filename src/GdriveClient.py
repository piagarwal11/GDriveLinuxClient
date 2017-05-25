
from __future__ import print_function
import httplib2
import os

from apiclient import discovery

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import optparse
import hashlib
import json
from _ast import Str
import glob
from apiclient.http import MediaFileUpload

import sys
from mimetypes import MimeTypes
import urllib
from apiclient import errors


# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client-secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
home_dir = os.path.expanduser('~');
    








def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials




    
    

        
    
    
    
    



# Util Functions
    



def getmd5(file):
    return hashlib.md5(open(file, 'rb').read()).hexdigest()
 
def createDriveFolder(service):
    file_metadata = {
        'name' : 'Invoices',
        'mimeType' : 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,fields='id').execute()
    print ('File ID: %s' % file.get('id'))
    
    # create a folder in system
    folder_name = 'Drive'
    path = os.path.join(home_dir, folder_name)
    folder_path = makeSystemFolder(folder_name, home_dir)
    dictionary = dict();
    dictionary['id'] = file.get('id')
    metadatafile_path = os.path.join(folder_path, '.metadata')
    metadata_file = open(metadatafile_path, 'r+');
    serialized = json.dumps(dictionary)
    metadata_file.write(serialized)
    metadata_file.flush()
    
    
def createreport(service, folder_path):
    report = [];
    print('i am inside create report')
    dictionary = dict()    
    status_file_path = os.path.join(folder_path, '.status')
    status_file = open(status_file_path, 'r+')
    status =  None
    try:
        status = json.loads(status_file.read())
    except (ValueError):
         
        status = None    
    status_file.close()
    
   
#     for val in npacked.keys():
#         print(npacked[val])
    dirs = glob.glob(folder_path +'/*')
#     dirs = os.listdir(path);
    for path_ in dirs:
        file = open(path_,'r+')
        file_name  = os.path.basename(file.name)
        if not file.name.startswith('.'):
            dictionary[file_name] = File(file_name,None, None, status[file_name]['driveid'], getmd5(path_)).__dict__
            if not status == None:
                if not status[file_name]['md5'] == getmd5(path_):
                    print(file_name + " is changed")
                    report_item = File(file_name, 'upload', 'added', status[file_name]['driveid'])
                    report.append(report_item.__dict__)
                else:
                    print(file_name + " is not changed")
                    report_item = File(file_name, None, 'untouched', status[file_name]['driveid'])
                    report.append(report_item.__dict__)
        
    print(json.dumps(report))
    return report
    
#     serialized = json.dumps(dictionary)
#     
#     status_file = open(status_file_path, 'w')
#     status_file.write(serialized)
#     status_file.flush()
#     status_file.close()
#    

def sync(service, folder_path):
    
        metadata_file = open(os.path.join(folder_path, '.metadata'), 'r')
        metadata = json.loads(metadata_file.read())
        print('parent_id' + metadata['id'])
        parent_id = metadata['id']
        status_file_path = os.path.join(folder_path, '.status')
        status_file = open(status_file_path, 'r+')
        status =  None
        try:
            status = json.loads(status_file.read())
        except (ValueError):
            status = None    
        status_file.close()
        
        report = createreport(service, os.path.join(home_dir, 'Drive') )
        
        for item in report :
            mime = MimeTypes()
            url = urllib.pathname2url(os.path.join(folder_path, item['name']))
            mime_type = mime.guess_type(url)
            mime = mime_type[0]
            if mime_type[0]== None:
                mime = 'text/plain'
            if not item['driveid']==None:
                trashDriveFile(service, item['driveid'])
            file_id = uploadfile(service,item['name'], item['driveid'], mime, os.path.join(folder_path, item['name']), parent_id)
            status[item['name']]['driveid']  = file_id
            
        serialized = json.dumps(status)
        status_file = open(status_file_path, 'w')
        status_file.write(serialized)
        status_file.flush()
        status_file.close()
            
def uploadfile(service, name , drive_id, mime, file_path, parent_id):
#     file_metadata = { 'name' : name }
#     media = MediaFileUpload(file_path,
#                         mimetype=mime)
#     file = service.files().create(body=file_metadata,
#                                     media_body=media,
#                                     fields='id').execute()
#     print ('File ID: %s' % file.get('id'))  
    
    folder_id = parent_id
    file_metadata = {
        'name' : name,
        'parents': [ folder_id ]
#          ,'id':drive_id 
    }
    media = MediaFileUpload(file_path,
                        mimetype=mime,
                        resumable=True)
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
                                    
    file = service.files().delete()
    
    print ('File ID: %s' % file.get('id'))      
    return file.get('id')    

def trashDriveFile(service, file_id):
    print ('trashing file ' + file_id)
    try:
        return service.files().delete(fileId=file_id).execute()   #trash(fileId=file_id).execute()
    except (errors.HttpError):
        print ('An error occurred while trashing')
        
        
def iterateonFiles(path, file_path):
    return path
    
def makeSystemFolder(name, path):
    path = os.path.join(path, name)
    try:
        os.makedirs(path);
    except OSError, e:
        print ('folder already present')
        answer = raw_input("Do you want to continue with this folder Yes/No?")
        if(answer == 'No'):
            sys.exit(1)
    # make a metadata file inside this folder, which stores data related to drive
    print('making metadata file at' +  path)
    makeSystemFile('.metadata', path)
    return path
    
def makeSystemFile(name, path):
      file_path = os.path.join(path, name)
      if not os.path.exists(file_path):
        file = open(file_path, 'w+')
        file.flush()
        file.close()
          

# Main function

class File :
    
   driveid = None
   name = None
   action = None
   status = None # modified, added, deleted, untouched
   md5 = None   
   

   def __init__(self, name, action = None, status = None, driveid=None, md5 = None):
      self.name = name
      self.action = action
      self.status = status
      self.driveid = driveid
      self.md5 = md5
      
    



def main():

     credentials = get_credentials()
     http = credentials.authorize(httplib2.Http())
     service = discovery.build('drive', 'v3', http=http)
#     
#     results = service.files().list(
#         pageSize=10,fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print('{0} ({1})'.format(item['name'], item['id']))
#     
    
     if options.folder:
        createDriveFolder(service)
        
     if options.file:
         uploadfile(service)   
         
     if options.sysfolder:
         makeSystemFolder('pp', '/home/piyush') 
         
     if options.report:
         createreport(service, os.path.join(home_dir, 'Drive')) 
     if options.sync:
         sync(service, os.path.join(home_dir, 'Drive')) 

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--folder',action="store_true", dest='folder', help='Create folder')
    parser.add_option('--sysfolder',action="store_true", dest='sysfolder', help='Create folder')
    parser.add_option('-F', '--file',action="store_true", dest='file', help='upload file')
    parser.add_option('-r', '--report',action="store_true", dest='report', help='create report')
    parser.add_option('-s', '--sync',action="store_true", dest='sync', help='sync folder')
    (options, args) = parser.parse_args()
    print (options.folder)
    main()