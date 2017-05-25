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





class Abcd :
    
   driveid = 0
   name = "xyz"
   action = 'Download'
   status = 'modified'   # modified, added, deleted, untouched
   

   def __init__(self, name, action, status, driveid):
      self.name = name
      self.action = action
      self.status = status
      self.driveid = driveid


abcd1 =  Abcd('piyush', 'upload', 'untouched', '1234')
abcd2 =  Abcd('piyush2', 'upload2', 'untouched2', '1234')

list = []

list.append(abcd1.__dict__)
list.append(abcd2.__dict__)
 
print(json.dumps(list))




