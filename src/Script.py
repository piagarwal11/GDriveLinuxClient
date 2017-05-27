#!/usr/bin/python

#24th May
#take input DONE
#create directory DONE
#save to system variable  
#how to write a service
#make an account in google drive


import sys; import os;
import subprocess;
import json
from celery.bin.celery import status
print (sys.version)

# x = raw_input("enter username")
# print 'kaa be'
# y = raw_input("enter path")
# 
# if x == 'piyush':
#     print 'you are logged in now'


# if os.path.exists(y):
#     path = os.path.join(y,"newDir")
#     print 'here'    
#     print path
#     os.makedirs(path)
#     print 'dir made'
# else:
#     print 'path not found'
# 
# subprocess.call("ls -l",shell=True)
# 
# subprocess.call('tail -f /home/piyush/dump.sql', shell=True)





#output = subprocess.Popen(['tail', '-100', '/home/piyush/piyush'], stdout=subprocess.PIPE)



import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
import Queue
import threading
import time

queueLock = threading.Lock()
workQueue = Queue.Queue(0)
thread = None

class LoggingEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""
#     makeSystemFile('.report', '/home/piyush/Drive')
    
        
    
    def on_moved(self, event):
        print('moved ' + event.dest_path + " " + event.src_path )
        
        
#         Action(event,'deleted')
#         Action(event,'moved')
#         
        queueLock.acquire()
        workQueue.put('moved ' + event.src_path + event.dest_path  )
        queueLock.release()
        
         
    
    def on_created(self, event):
#           print('created ' + event.src_path)
#           Action(event,'created') 

        queueLock.acquire()
        workQueue.put('created ' + event.src_path  )
        queueLock.release()
        
    def on_deleted(self, event):
#         print('deleted ' + event.src_path)
#         Action(event, 'deleted')  
        
        queueLock.acquire()
        workQueue.put('deleted ' + event.src_path   )
        queueLock.release()

    
    def on_modified(self, event):
#         print('modified ' + event.src_path)
#         if not event.is_directory:
#             Action(event, 'modified')
#         
        queueLock.acquire()
        workQueue.put('modified ' + event.src_path   )
        queueLock.release()
    
    

def makeSystemFile(name, path):
      file_path = os.path.join(path, name)
      if not os.path.exists(file_path):
        file = open(file_path, 'w+')
        file.flush()
        file.close()



class Action:
    
            
    def __init__(self, event, action):
        
        file_path = None
        if action == 'moved':
            file_path = event.dest_path
        else:
            file_path = event.src_path
            
        if ((os.path.basename(file_path)).startswith('.')):
            return
        report_file = open('/home/piyush/Drive/.report', 'r')
        data = report_file.read()
        report_file.close()
        print('------------')
        print(data)
        print('------------')
        report =  dict()
        try:
            report = json.loads(data)
        except ValueError, e:
            print (str(e))
            report = dict()    
        
            
        report[file_path] = File(os.path.basename(file_path), 'upload', action, None, None, event.is_directory).__dict__
        report_file = open('/home/piyush/Drive/.report', 'w')
        report_file.write(json.dumps(report))
        report_file.flush()
        report_file.close()




    
    
 



class File :
    
   driveid = None
   name = None
   action = None
   status = None # modified, added, deleted, untouched
   md5 = None   
   is_dir = None
   parent_id  = None
   

   def __init__(self, name, action = None, status = None, driveid=None, md5 = None, is_dir = None, parent_id = None):
      self.name = name
      self.action = action
      self.status = status
      self.driveid = driveid
      self.md5 = md5
      self.is_dir = is_dir
      self.parent_id = parent_id
      
      
class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print "Starting " + self.name
      process_data(self.name, self.q)
      print "Exiting " + self.name

def process_data(threadName, q):
   while True:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)      
      















if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
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






