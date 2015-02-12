"""This tests the scraping of JSON search results from the Tisch Library website."""

import csv
import json
import re
import requests
import sys


COOKIE = {'Summon-Two': 'TRUE'}
BASE_URL = 'http://tufts.summon.serialssolutions.com/api/search?pn=1&ho=t&q='
SSL_CSV_FILE = 'isbnscraped.csv'


def retrieve_search_results(entry, writer):
  """Sends a query for items with the given title to the Tisch Library website."""
  r = requests.get(BASE_URL + entry['title'], cookies=COOKIE)

  # Attempt to retrieve JSON from response
  try:
    full_search_results = r.json()
  except ValueError as e:
    sys.stderr.write('%s %s: %s\n' % (entry['browsepath'], entry['title'], e))
    writer.writerow(entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], None)
    return

  # Determine if there are any documents to deal with
  documents = full_search_results['documents']
  if len(documents) == 0:
    sys.stderr.write('%s %s: No results found on Tisch Library\n' % (entry['browsepath'], entry['title']))
    writer.writerow(entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], None)
    return

  # Figure out if any of them are the one we want
  for doc in documents:
    try:
      # Check ISBN
      for doc_isbn in doc['issns'] + doc['eissns']:
        if entry['isbn'] == doc_isbn:
          # Found match
          writer.writerow(entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], doc)
          return
      # Check titles by comparing only uppercase alpha(numeric) characters
      doc_title = doc['title'].replace('<b>', '').replace('</b>', '').upper()
      ssl_title = entry['title'].upper()
      re.sub(r'\W+', '', doc_title)
      re.sub(r'\W+', '', ssl_title)
      if doc_title != ssl_title:
        continue
      # Check authors
      for doc_author in doc['authors']:
        doc_author_last, doc_author_first = doc_author['fullname'].strip().split(',')
      if (doc_author_last in entry['authors']) and (doc_author_first in entry['authors']):
        # Found match
        writer.writerow(entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], doc)
        return
    except:
      # Some entry we tried to use doesn't exist
      sys.stderr.write('%s %s: %s\n' % (entry['browsepath'], entry['title'], e))

  # No documents caused a match
  sys.stderr.write('%s %s: No results matched on Tisch Library\n' % (entry['browsepath'], entry['title']))
  writer.writerow(entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], None)


def read_input():
  """Parse the input CSV file to obtain data to search for."""
  title_list = []

  with open(SSL_CSV_FILE, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      # format of data is id, title, isbn, authors, browsepath
      title_list.append({'id': row[0],
                         'title': row[1]),
                         'isbn': row[2],
                         'authors': row[3],
                         'browsepath': row[4]})
  return title_list


def main():
  """Queries the Tisch Library catalogs to retrieve citation information."""
  ssl_entries = read_input()

  with open('tischdata.csv', 'wb') as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
    # output format is id, browsepath, SSL title/isbn/authors, Tisch JSON
    writer.writerow('Id', 'Browsepath', 'SSL Title', 'SSL Author', 'SSL ISBN', 'Tisch JSON')
    for entry in ssl_entries:
      retrieve_search_results(entry, writer)


if __name__ == '__main__':
  main()
