#!/usr/bin/python

#24th May
#take input DONE
#create directory DONE
#save to system variable  
#how to write a service
#make an account in google drive


import sys; import os;
import subprocess;
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

subprocess.call("ls -l",shell=True)

subprocess.call('tail -f /home/piyush/dump.sql', shell=True)





#output = subprocess.Popen(['tail', '-100', '/home/piyush/piyush'], stdout=subprocess.PIPE)








