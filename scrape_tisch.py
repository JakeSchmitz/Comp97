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
    pass
  try:
    doc_isbns += doc['eissns']
  except KeyError as e:
    pass
  try:
    doc_isbns += doc['isbns']
  except KeyError as e:
    pass
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
    pass
  return False

def retrieve_search_results(entry, writer):
  """Sends a query for items with the given title to the Tisch Library website."""
  r = requests.get(BASE_URL + entry['title'], cookies=COOKIE)

  # Attempt to retrieve JSON from response
  try:
    full_search_results = r.json()
  except ValueError as e:
    print('%s, %s, %s, %s' % (entry['id'], entry['browsepath'], entry['title'], e))
    return

  # Determine if there are any documents to deal with
  documents = full_search_results['documents']
  if len(documents) == 0:
    print('%s, %s, %s, No results found on Tisch Library' % (entry['id'], entry['browsepath'], entry['title']))
    return

  # Figure out if any of them are the one we want
  for doc in documents:
    if compare_isbn(entry, doc) or compare_title_author(entry, doc):
      # This is the result that matches the SSL entry--print metadata one field at a time
      metadata = doc.items()
      metadata.sort(key=lambda tup: tup[0])
      writer.writerow([entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn']] + metadata)
      return

  # No documents caused a match
  print('%s, %s, %s, No results matched on Tisch Library' % (entry['id'], entry['browsepath'], entry['title']))


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

  with open('tischdata.csv', 'ab') as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
    if len(sys.argv) == 1:
      # no index list specified, so run on all entries
      writer.writerow(['Id', 'Browsepath', 'SSL Title', 'SSL Author', 'SSL ISBN', 'Tisch JSON'])
      i = 0
      for entry in ssl_entries:
        if i % 500 == 0:
          sys.stderr.write('done %d\n' % i)
        try:
          retrieve_search_results(entry, writer)
        except Exception as e:
          print('%s %s: Unhandled error %s' % (entry['id'], entry['title'], e))
        i += 1
    else:
      # run only on entries in list of indices
      index_filename = sys.argv[1]
      with open(index_filename, 'r') as infile:
        indices = [int(row) for row in infile]
        for i in indices:
          try:
            retrieve_search_results(ssl_entries[i], writer)
          except Exception as e:
            print('%s, %s, %s, Unhandled error %s' % (ssl_entries[i]['id'], ssl_entries[i]['browsepath'], ssl_entries[i]['title'], e))


if __name__ == '__main__':
  main()
