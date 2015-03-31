import sys
import re
import pymongo
import math
from pymongo import MongoClient
import csv
import json

class MongoWriter:
  def __init__(self, fname, mongourl, dbname, collection_name, rowcap=None):
    self.client = MongoClient(mongourl) 
    self.db = self.client.get_default_database()
    self.collection = self.db[collection_name]
    print 'connected to mongo instance'
    self.data = dict()
    with open(fname, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        if rowcap is not None and rowcap < i:
          break
        self.data[row[0]] = dict()
        doc_id = str(row[0])
        if int(int(row[0]) / 1000) == 0 and row[0] != '0':
          magnitude = int(math.floor(math.log10(abs(float(doc_id)))))
          for i in range(3 - magnitude):
            doc_id = '0' + doc_id
        elif row[0] == '0':
          doc_id = '0000'
        self.data[row[0]]['_id'] = str(doc_id)
        self.data[row[0]]['browsepath'] = row[1] 
        self.data[row[0]]['ssltitle'] = row[2]
        self.data[row[0]]['sslauthor'] = row[3]
        self.data[row[0]]['isbn'] = row[4]
        for c in row[5:]:
          try: 
            broken = c.split(',')
            k = '('.join(broken[0].split('(')[1:])
            v = ','.join(broken[1:]) if len(broken[1:]) > 1 else broken[1]
            v = ')'.join(v.split(')')[:-1])
            v = re.split('u[\'|\"]', v)
            if len(v) > 1:
              map(lambda word: word[:-1], v)
            val = []
            for x in v:
              if x is not None and x is not '':
                newx = x.replace('\'', '')
                if newx[0] == ' ' and len(newx) > 1:
                  newx = newx[1:]
                val.append(newx)
            if k.startswith('u\''):
              k = k[2:-1]
            val = ''.join(val)
            self.data[row[0]][k.encode('ascii', 'ignore')] = val.encode('ascii', 'ignore')
          except:
            print sys.exc_info()[1]
        self.data[row[0]]['id'] = str(doc_id)

  def test_write(self, num_rows=1):
    i = 0
    for k in self.data.keys():
      self.collection.insert(self.data[k])
      i += 1
      if i > num_rows:
        break

  def write_all_data(self):
    failures = {}
    for k in self.data.keys():
      try:
        self.collection.save(self.data[k])
      except pymongo.errors.DuplicateKeyError: 
        failures[self.data[k]['_id']] = sys.exc_info()[1]
        print sys.exc_info()[1]
      except:
        failures[self.data[k]['_id']] = sys.exc_info()[1]
        print sys.exc_info()[1]
    return failures
 #     except:
  #      print 'Failed to write record to mongo ' + str(self.data[k]['id'])
   #   finally:
    #    i += 1
     #   if i >= num_rows:
      #   break

username = ''
password = ''            
dbname = ''
collect = ''
if len(sys.argv) > 4:
  username = sys.argv[1]
  password = sys.argv[2]
  dbname = sys.argv[3]
  collect = sys.argv[4]
else:
  print 'Please provide username, password, dbname, and collection name via the command line'
  exit()
mw = MongoWriter('tischdata.csv', 'mongodb://' + username + ':' + password + '@ds047591.mongolab.com:47591/heroku_app34131114', dbname, collect)
print mw.write_all_data()   

