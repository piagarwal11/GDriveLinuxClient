
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



def createFolder(service):
    
    
    
    file_metadata = {
        'name' : 'Invoices',
        'mimeType' : 'application/vnd.google-apps.folder'
    }
#     file = service.files().create(body=file_metadata,fields='id').execute()
#     print ('File ID: %s' % file.get('id'))
#     
    # create a folder in system
    home_dir = os.path.expanduser('~');
    folder_name = 'Drive'
    path = os.path.join(home_dir, folder_name)
    if os.path.exists(path) == False:
            os.makedirs(path, 0777);
    file_path = os.path.join(path, '.status')
    print(file_path)
    if not os.path.exists(file_path):
        status_file = open(file_path, 'w+')
        status_file.flush()
        status_file.close()
    
    iterateonFiles(path, file_path)
    
    
    
    
def iterateonFiles(path, file_path):
    print('i am inside file iteration')
    dictionary = dict()    
    status_file = open(file_path, 'r+');
    
    text = status_file.read();
#     print(text)
    npacked = json.loads(text);
#     for val in npacked.keys():
#         print(npacked[val])
    
    
    dirs = glob.glob(path +'/*.*')
#     dirs = os.listdir(path);
    for path_ in dirs:
        file = open(path_,'r+')
        name  = os.path.basename(file.name)
        if not file.name.startswith('.'):
            dictionary[file] = getmd5(path_)
            if not npacked[name] == getmd5(path_):
                print(name + " is changed")
    

#     serialized = json.dumps(dictionary)
    
#     status_file.write(serialized)
#     status_file.flush()
#    
    
def uploadfile(service):
    file_metadata = { 'name' : 'photo.jpg' }
    media = MediaFileUpload('/home/piyush/Pictures/Wallpapers/286384.jpg',
                        mimetype='image/jpeg')
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print ('File ID: %s' % file.get('id'))


def getmd5(file):
    return hashlib.md5(open(file, 'rb').read()).hexdigest()
 
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
        createFolder(service)
        
     if options.file:
         uploadfile(service)   

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--folder',action="store_true", dest='folder', help='Create folder')
    parser.add_option('-F', '--file',action="store_true", dest='file', help='upload file')
    (options, args) = parser.parse_args()
    print (options.folder)
    main()