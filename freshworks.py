#data store in 'album2.txt'
#windows 10 preferred
import threading#python 3 and above
from threading import*
import time
import json
import os
import sys

dt={} #'dt' is the dictionary 

#create operation 
#syntax "freshworks.create(key,value,timeout_in_sec)"
#syntax "freshworks.create(key,value)"
#timeout can be declared or neglected to zero
#timeout 0 will not lead to deletion after 0 sec
class freshworks:
  path='album2.txt'
  isExist = os.path.exists(path)  
  if(isExist):
   def create(key,value,timeout=0):
       with open('album2.txt') as f: #open file and load
               js = f.read()
               dt = json.loads(js)
       if key in dt:
          print("key already exists") #printing error
       else:
           if(key.isalpha()):
               if sys.getsizeof(value)<=(16*1024): #Jasonobject value less than 16KB 
                   if timeout==0:
                       l=[value,timeout]
                   else:
                       l=[value,time.time()+timeout]
                   if len(key)<=32:#input key_name at most 32chars
                       dt[key]=l
                       f = open("album2.txt", "w")#open file and update
                       json.dump(dt,f)
                       if(os.stat('album2.txt').st_size>(1024*1024*1024)):
                           print("File memory exceeded!!")#File size greater than 1GB
                           freshworks.delete(key)
               else:
                   print("Value limit exceeded!! ")#printing error
           else:
               print("Invalid key_name! ENTER key_name must contain only alphabets")#printing error
  else:
   def create(key,value,timeout=0):
       if key in dt:
          print("key already exists") #printing error
       else:
           if(key.isalpha()):
               if len(dt)<(1024*1024*1024) and sys.getsizeof(value)<=(16*1024): #file size less than 1GB and Jasonobject value less than 16KB 
                   if timeout==0:
                        l=[value,timeout]
                   else:
                       l=[value,time.time()+timeout]
                   if len(key)<=32: #input key_name at most 32chars
                      dt[key]=l
                      f = open("album2.txt", "w")#open new file and update
                      json.dump(dt,f)
               else:
                   print("error: Memory limit exceeded!! ")#printing error
           else:
               print("Invalid key_name! ENTER key_name must contain only alphabets")#printing error

    
#read
#syntax "freshworks.read(key)"
            
  def read(key):
      with open('album2.txt') as f:  #open file and load
               js = f.read()
               dt = json.loads(js)
      if key not in dt:
          print("given key does not exist in data store. Please enter a valid key") #printing error
      else:
          b=dt[key]
          if b[1]!=0:
              if time.time()<b[1]: #comparing the present time with expiry time
                  string=str(key)+":"+str(b[0]) #return the value in the format of JasonObject i.e.,"key_name:value"
                  return string
              else:
                  freshworks.delete(key)#time-to-live extict
          else:
              string=str(key)+":"+str(b[0])
              return string

#delete
#syntax "freshworks.delete(key)"

  def delete(key):
      with open('album2.txt') as f:  #open file and load
               js = f.read()
               dt = json.loads(js)
      if key not in dt:
          print("given key does not exist in data store. Please enter a valid key") #printing error
      else:
          b=dt[key]
          if b[1]!=0:
              if time.time()<b[1]: #comparing the current time with expiry time
                  del dt[key]
                  f = open("album2.txt", "w")  #open file and update
                  json.dump(dt,f)
                  print("key is deleted")
              else:
                  del dt[key]
                  f = open("album2.txt", "w")
                  json.dump(dt,f)
                  print("time-to-live of",key,"has expired") #printing error once for an json object
          else:
              del dt[key]
              f = open("album2.txt", "w")
              json.dump(dt,f)
              print("key is deleted")

