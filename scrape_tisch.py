"""This tests the scraping of JSON search results from the Tisch Library website."""

import csv
import json
import re
import requests
import sys


COOKIE = {'Summon-Two': 'TRUE'}
BASE_URL = 'http://tufts.summon.serialssolutions.com/api/search?pn=1&ho=t&q='
SSL_CSV_FILE = 'isbnscrape.csv'


def retrieve_search_results(entry, writer):
  """Sends a query for items with the given title to the Tisch Library website."""
  r = requests.get(BASE_URL + entry['title'], cookies=COOKIE)

  # Attempt to retrieve JSON from response
  try:
    full_search_results = r.json()
  except ValueError as e:
    print('%d %s: %s\n' % (entry['id'], entry['title'], e))
    writer.writerow([entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], None])
    return

  # Determine if there are any documents to deal with
  documents = full_search_results['documents']
  if len(documents) == 0:
    print('%d %s: No results found on Tisch Library\n' % (entry['id'], entry['title']))
    writer.writerow([entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], None])
    return

  # Figure out if any of them are the one we want
  for doc in documents:
    # Check ISBN
    doc_isbns = []
    try:
      doc_isbns += doc['issns']
    except KeyError:
      pass
    try:
      doc_isbns += doc['eissns']
    except KeyError:
      pass
    for doc_isbn in doc_isbns:
      if entry['isbn'] == doc_isbn:
        # Found match
        writer.writerow([entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], doc])
        return
    # If no ISBN match, check titles by comparing only uppercase alpha(numeric) characters
    try:
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
        writer.writerow([entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], doc])
        return
    except KeyError as e:
      # Some entry we tried to use doesn't exist
      print('%d %s: %s\n' % (entry['id'], entry['title'], e))

  # No documents caused a match
  print('%d %s: No results matched on Tisch Library\n' % (entry['id'], entry['title']))
  writer.writerow([entry['id'], entry['browsepath'], entry['title'], entry['authors'], entry['isbn'], None])


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
