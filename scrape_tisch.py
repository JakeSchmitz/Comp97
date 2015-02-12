"""This tests the scraping of JSON search results from the Tisch Library website."""

import csv
import json
import re
import requests
import sys


COOKIE = {'Summon-Two': 'TRUE'}
BASE_URL = 'http://tufts.summon.serialssolutions.com/api/search?pn=1&ho=t&q='
SSL_CSV_FILE = 'isbnscrape.csv'


def compare_isbn(entry, doc):
  """Use ISBNs to determine if doc is the entry from SSL."""
  doc_isbns = []
  try:
    doc_isbns += doc['issns']
  except KeyError as e:
    print('%s %s: %s\n' % (entry['id'], entry['title'], e))
  try:
    doc_isbns += doc['eissns']
  except KeyError as e:
    print('%s %s: %s\n' % (entry['id'], entry['title'], e))
  for doc_isbn in doc_isbns:
    if entry['isbn'] == doc_isbn:
      # Found match
      return True
  return False


def compare_title_author(entry, doc):
  """Use title and author to determine if doc is entry from SSL."""
  try:
    doc_title = doc['title'].replace('<b>', '').replace('</b>', '').upper()
    ssl_title = entry['title'].upper()
    re.sub(r'\W+', '', doc_title)
    re.sub(r'\W+', '', ssl_title)
    # Check titles
    if (doc_title != ssl_title) and (doc_title not in ssl_title) and (ssl_title not in doc_title):
      return False
    # Check authors
    for doc_author in doc['authors']:
      author_parts = doc_author['fullname'].split()
      for part in author_parts:
        re.sub(r'\W+', '', part)
        if part not in entry['authors']:
          return False
    # All authors from Tisch are in the SSL entry
    # TODO: Should we mark the document as a match if all of one of the authors match?
    return True
  except KeyError as e:
    # Some entry we tried to use doesn't exist
    print('%d %s: %s\n' % (entry['id'], entry['title'], e))
  return False

def retrieve_search_results(entry, writer):
  """Sends a query for items with the given title to the Tisch Library website."""
  r = requests.get(BASE_URL + entry['title'], cookies=COOKIE)

  # Attempt to retrieve JSON from response
  try:
    full_search_results = r.json()
  except ValueError as e:
    print('%d %s: %s' % (entry['id'], entry['title'], e))
    return

  # Determine if there are any documents to deal with
  documents = full_search_results['documents']
  if len(documents) == 0:
    print('%d %s: No results found on Tisch Library' % (entry['id'], entry['title']))
    return

  # Figure out if any of them are the one we want
  for doc in documents:
    if compare_isbn(entry, doc) or compare_title_author(entry, doc):
      writer.writerow([entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], doc])
      return

  # No documents caused a match
  print('%d %s: No results matched on Tisch Library' % (entry['id'], entry['title']))


def read_input():
  """Parse the input CSV file to obtain data to search for."""
  title_list = []

  with open(SSL_CSV_FILE, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      # format of data is id, title, isbn, authors, browsepath
      try:
        entry = {'id': row[0],
                 'title': row[1],
                 'isbn': row[2],
                 'authors': row[3],
                 'browsepath': row[4]}
      except IndexError as e:
        print('Invalid row %s\n' % row)
      else:
        title_list.append(entry)
  return title_list


def main():
  """Queries the Tisch Library catalogs to retrieve citation information."""
  ssl_entries = read_input()

  with open('tischdata.csv', 'wb') as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
    # output format is id, browsepath, SSL title/isbn/authors, Tisch JSON
    writer.writerow(['Id', 'Browsepath', 'SSL Title', 'SSL Author', 'SSL ISBN', 'Tisch JSON'])
    i = 0
    for entry in ssl_entries:
      if i % 500 == 0:
        sys.stderr.write('done %d\n' % i)
      retrieve_search_results(entry, writer)
      i += 1


if __name__ == '__main__':
  main()
