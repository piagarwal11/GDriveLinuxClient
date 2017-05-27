
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
import Script
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
import Queue
import threading
import time
from watchdog.observers import Observer
from mercurial.util import readfile

#26 May - send all changes from system to drive


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
folder_path = '/home/piyush/Drive' 

    
queueLock = threading.Lock()
workQueue = Queue.Queue(0)
thread = None
service  = None






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
         
        status = dict()    
    status_file.close()
    
   
#     for val in npacked.keys():
#         print(npacked[val])
    dirs = glob.glob(folder_path +'/*')
#     dirs = os.listdir(path);
    for path_ in dirs:
        if os.path.isdir(path_):
            continue
        file = open(path_,'r')
        file_name  = os.path.basename(file.name)
        if status.has_key(file_name): 
            print ('sdfdsfdsfdss ' + file_name)
            drive_id =  status[file_name]['driveid']
        else:
            drive_id = None
        if not file.name.startswith('.'):
            dictionary[file_name] = File(file_name,None, None, drive_id, getmd5(path_)).__dict__
            if status.has_key(file_name):
                if not status[file_name]['md5'] == getmd5(path_):
                    print(file_name + " is changed")
                    report_item = File(file_name, 'upload', 'added', drive_id)
                    report.append(report_item.__dict__)
                else:
                    print(file_name + " is not changed")
                    report_item = File(file_name, None, 'untouched', drive_id)
                    report.append(report_item.__dict__)
            else:
                print(file_name + " newly added")
                report_item = File(file_name, None, 'added', drive_id)
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
        if not os.path.exists(status_file_path):
            open(status_file_path, 'w+').close()
            
        status_file = open(status_file_path, 'r+')
        status =  None
        try:
            status = json.loads(status_file.read())
        except (ValueError):
            status = dict()    
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
            if(status.has_key(item['name'])):
                status[item['name']]['driveid']  = file_id
            else:
                 status[item['name']] = File(item['name'],None, None, file_id, getmd5(os.path.join(folder_path, item['name']))).__dict__   
            
        serialized = json.dumps(status)
        status_file = open(status_file_path, 'w')
        status_file.write(serialized)
        status_file.flush()
        status_file.close()
            
def uploadfile(service, name = None , drive_id = None, mime = None, file_path=None, parent_id = None):
#     file_metadata = { 'name' : "pp" }
#     media = MediaFileUpload('/home/piyush/Drive/piyush',
#                         mimetype='text/plain')
#     file = service.files().create(body=file_metadata,
#                                     media_body=media,
#                                     fields='id').execute()
#     print ('File ID: %s' % file.get('id'))  
    print(parent_id)
    print('anme ' + name)
    print('mime' + mime)
    print('file_path' + file_path)
#     
    folder_id = parent_id
    file_metadata = {
        'name' : name,
        'parents': [ parent_id ]
#          ,'id':drive_id 
    }
    media = MediaFileUpload(file_path,
                        mimetype=mime,
                        resumable=True)
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
                                     
    
    
    print ('File ID: %s' % file.get('id'))      
    return file.get('id')   

def createDriveFolder(service , name, parent_id):
    file_metadata = {
        'name' : name,
        'mimeType' : 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    file = service.files().create(body=file_metadata,fields='id').execute()
    print ('File ID: %s' % file.get('id'))
    return file.get('id')
    # create a folder in system
#     folder_name = 'Drive'
#     path = os.path.join(home_dir, folder_name)
#     if not (os.path.exists(path)):
#         folder_path = makeSystemFolder(folder_name, home_dir)
#     
     



def trashDriveFile(service, file_id):
    if file_id == None:
        return
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
#     makeSystemFile('.report', path)
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
   is_synced = False
   is_dir = False   
   

   def __init__(self, name=None, action = None, status = None, driveid=None, md5 = None, is_synced=False, is_dir = False):
      self.name = name
      self.action = action
      self.status = status
      self.driveid = driveid
      self.md5 = md5
      self.is_synced = is_synced
      self.is_dir = is_dir
      

class LoggingEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""
#     makeSystemFile('.report', '/home/piyush/Drive')
    
        
    
    def on_moved(self, event):
        print('moved ' + event.src_path + " " + event.dest_path )
        
        
        if not str(event.src_path).find('.goutputstream') == -1:
            Action(event.src_path, event.dest_path, event.is_directory, 'modified')
        else:
            Action(event.src_path, event.dest_path, event.is_directory,'deleted')
            Action(event.src_path, event.dest_path, event.is_directory,'moved')
         
#         
        
         
    
    def on_created(self, event):
        print('created ' + event.src_path)
        Action(event.src_path, None, event.is_directory,'created') 

        
    def on_deleted(self, event):
        print('deleted ' + event.src_path)
        Action(event.src_path, None, event.is_directory,'deleted')  
        
        
    
    def on_modified(self, event):
        return
#         print('modified ' + event.src_path)
#         if not event.is_directory:
#             Action(event, 'modified')


class Action:
    
            
    def __init__(self, src_path, dest_path, is_dir, status):
        
        print('Action is ' + status)
        file_path = None
        if status == 'moved' or status == 'modified':
            file_path = dest_path
        else:
            file_path = src_path
            
        if ((os.path.basename(file_path)).startswith('.')):
            return
        report = dict()
        report = readFile('/home/piyush/Drive/.report')
        
        file = File().__dict__
        if report.has_key(file_path):
            file = report[file_path]
        report[file_path] = File(file_path, 'upload', status, file['driveid'] , file['md5'], False,is_dir).__dict__
        writeFile('/home/piyush/Drive/.report', json.dumps(report))
        
        
        #change in drive
        print('here')
#         queueLock.acquire()
        print('here2')
        workQueue.put(report[file_path])
#         queueLock.release()
        
        
           
        

def readFile(path):
    if not os.path.exists(path):
        report_file = open(path, 'w+').close()
    report_file = open(path, 'r')
    try:
        data = json.loads(report_file.read())
    except ValueError, e:
        print(str(e))
        data = dict()  
    report_file.close()    
    return data

def writeFile(path, data):
    report_file = open(path, 'w+')
    report_file.write(data)
    report_file.flush()
    report_file.close()    
    


    
class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.q)
      print ("Exiting " + self.name)

def process_data(threadName, q):
   while True:
#         queueLock.acquire()
        if not workQueue.empty():
            file = q.get()
            print('thread performing ' + file['status'] )
            report = dict()
            report = readFile('/home/piyush/Drive/.report')
            
#             send file to drive
            parent_id = getParentid(report, file['name'])
            if parent_id == None:
                print('parent_id not found')
#                 queueLock.release()
                
                continue
            mime = MimeTypes()
            url = urllib.pathname2url(file['name'])
            mime_type = mime.guess_type(url)
            mime = mime_type[0]
            if mime_type[0]== None:
                mime = 'text/plain'
            if file['status'] == 'created' and file['is_synced'] == False:
                if file['is_dir'] == False:
                    file_id = uploadfile(service, os.path.basename(file['name']), None, mime, file['name'],parent_id) 
                else:
                    file_id = createDriveFolder(service, os.path.basename(file['name']), parent_id)
                
                report[file['name']]['is_synced'] = True
                report[file['name']]['driveid'] = file_id
            elif file['status'] == 'deleted' and file['is_synced'] == False:
                trashDriveFile(service, file['driveid'])   
                report[file['name']]['is_synced'] = True
            elif file['status'] == 'moved' and file['is_synced'] == False:
                if file['is_dir'] == False:
                    file_id = uploadfile(service, os.path.basename(file['name']), None, mime, file['name'],parent_id) 
                else:
                    file_id = createDriveFolder(service, os.path.basename(file['name']), parent_id)
                
                report[file['name']]['is_synced'] = True
                report[file['name']]['driveid'] = file_id
            elif file['status'] == 'modified' and file['is_synced'] == False:
                trashDriveFile(service, file['driveid']) 
                file_id = uploadfile(service, os.path.basename(file['name']), None, mime, file['name'],parent_id) 
                report[file['name']]['is_synced'] = True
                report[file['name']]['driveid'] = file_id
            
            writeFile('/home/piyush/Drive/.report', json.dumps(report))
            
#             queueLock.release()
            print ("%s processing %s" % (threadName, file['name'] +' ' +file['status']))
#         else:
#             queueLock.release()
        time.sleep(1)      

      
      
def getParentid(report, path):
    parent_path = os.path.abspath(os.path.join(path, os.pardir));
    print('parnet_path ' + parent_path)
    if str(parent_path).find(folder_path) > -1:
        print('parent path is valid')
        if not report.has_key(parent_path):
            print('created ' + parent_path)
#            Action(parent_path, None, True,'created')
            return None
        else:    
            parent_drive_id = report[parent_path]['driveid']
            if parent_drive_id == None:
                return None
                
            else:
                print("pdi " + parent_drive_id)
                return parent_drive_id
             
    
    return None


def main():

     credentials = get_credentials()
     http = credentials.authorize(httplib2.Http())
     global service
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
         
      
     report = dict()
     report = readFile('/home/piyush/Drive/.report')  
     report['/home/piyush/Drive'] = File('/home/piyush/Drive', 'upload', 'created', '0BxW128bZHQogWWVRb3l3eXg1RVk' , None, True, True).__dict__
     writeFile('/home/piyush/Drive/.report', json.dumps(report))    
         

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--folder',action="store_true", dest='folder', help='Create folder')
    parser.add_option('--sysfolder',action="store_true", dest='sysfolder', help='Create folder')
    parser.add_option('-F', '--file',action="store_true", dest='file', help='upload file')
    parser.add_option('-r', '--report',action="store_true", dest='report', help='create report')
    parser.add_option('-s', '--sync',action="store_true", dest='sync', help='sync folder')
    
    (options, args) = parser.parse_args()
#     print (os.path.abspath(os.path.join('/home/piyush/Drive', os.pardir)))
    
    main()
    path = folder_path
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    thread = myThread(1, "Sync_guy", workQueue)
    thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
    
    