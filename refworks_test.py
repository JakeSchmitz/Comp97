"""Tests the connection to the RefWorks API.

Eventually, this will be a class-based wrapper for the API.
"""

import datetime
import hmac
import httplib
import logging
import requests
import time
import urllib

from hashlib import sha1
from secrets import *


def generate_signature(class_name, access_key, secret_key):
  """Generates the signature required for all API calls"""
  expires = int(time.mktime(datetime.datetime.now().timetuple())) * 1000
  raw_signature = class_name + access_key + str(expires)
  signature = hmac.new(secret_key, raw_signature, sha1).digest().encode('base64').rstrip('\n')
  return {'class': class_name, 'accesskeyid': access_key, 'expires': expires, 'signature': signature}



def make_session():
  """Initiates an API session"""
  base_url = 'https://www.refworks.com/api2/'
  params = generate_signature('authentication', ACCESS_KEY_ID, SECRET_ID)
  params.update({'method': 'newsess'})
  xml = ('<AcctInfo>'
         '<groupCode>%s</groupCode>'
         '<loginName>%s</loginName>'
         '<password>%s</password>'
         '</AcctInfo>') % (GROUP_CODE, USERNAME, PASSWORD)
  r = requests.post(base_url, params=params, data=xml)
  print r.text


def init_logging():
  """Sets up error logging"""
  httplib.HTTPConnection.debuglevel = 1
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  requests_log = logging.getLogger('requests.packages.urllib3')
  requests_log.setLevel(logging.DEBUG)
  requests_log.propagate = True


def main():
  # init_logging()
  make_session()


if __name__ == '__main__':
  main()
