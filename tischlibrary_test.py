"""This tests the scraping of JSON search results from the Tisch Library website."""

import csv
import json
import random
import requests
import sys


COOKIE = {'Summon-Two': 'TRUE'}
BASE_URL = 'http://tufts.summon.serialssolutions.com/api/search?pn=1&ho=t&q='
CSV_FILE = 'ssl-data/ssldata.csv'


def retrieve_search_results(title):
  """Sends a query for items with the given title to the Tisch Library website."""
  r = requests.get(BASE_URL + title, cookies=COOKIE)
  try:
    content = json.loads(r.text)
  except:
    sys.stderr.write('ERROR: Results for "%s" could not be loaded to JSON.\n' % title)
  else:
    try:
      first_document = content['documents'][0]
    except:
      sys.stderr.write('ERROR: No results for "%s".\n' % title)
    else:
      try:
        # print json.dumps(first_document, sort_keys=True, indent=4, separators=(',', ': '))
        print first_document['title'].replace('<b>', '').replace('</b>', '')
      except:
        sys.stderr.write('ERROR: Could not get title for "%s".\n' % title)


def main():
  """Tests random articles from the SSL to make sure we can get valid output."""
  title_list = []

  with open(CSV_FILE, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      # title is the second entry in csv file
      title_list.append(row[1])

  sample = random.sample(xrange(len(title_list)), 100)
  for i in sample:
    if title_list[i] == 'SCRAPING ERROR':
      continue
    print title_list[i]
    retrieve_search_results(title_list[i])
    print ''


if __name__ == '__main__':
  main()
