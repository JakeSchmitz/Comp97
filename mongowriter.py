import sys
import pymongo
from pymongo import MongoClient
import csv

class MongoWriter:
  def __init__(self, fname, mongourl, rowcap=None):
    self.client = MongoClient(mongourl) 
    print 'connected to mongo instance'
    self.data = dict()
    with open(fname, 'rb') as f:
      reader = csv.reader(f)
      i = 0
      for row in reader:
        if rowcap is not None and rowcap < i:
          break
        self.data[row[0]] = dict()
        self.data[row[0]]['browsepath'] = row[1] 
        self.data[row[0]]['ssltitle'] = row[2]
        self.data[row[0]]['sslauthor'] = row[3]
        self.data[row[0]]['isbn'] = row[4]
        for c in row[5:]:
          try: 
            broken = c.split(',')
            k = broken[0]
            v = ','.join(broken[1:]) if len(broken[1:]) > 1 else broken[1]
            self.data[row[0]][k] = v
          except:
            print 'failed on ' + c
        i += 1
        print len(self.data[row[0]])

 
username = ''
password = ''            
if len(sys.argv) > 2:
  username = sys.argv[1]
  password = sys.argv[2]
mw = MongoWriter('tischdata.csv', 'mongodb://' + username + ':' + password + '@ds047591.mongolab.com:47591/heroku_app34131114')
   

