# The purpose of this file is to take the data scraped from the ssl
# server and use the article names to lookup bibliographic info from
# the tisch library website

# The ssl data is in csv format id, title, browsepath

import csv
import sys
import re
from bs4 import BeautifulSoup
import requests

input_file = sys.argv[1]
output_file = sys.argv[2]
invalid_title = "scraping error"
# Several different urls expose search, but it seems like different data sources are behind library and tufts domains
tisch_query_url = 'http://tufts.summon.serialssolutions.com/search?ho=t&s.q='
tisch_api_url = 'http://tufts.summon.serialssolutions.com/api/search?pn=1&amp;ho=t&amp;q='
tisch_old_url = 'http://library.tufts.edu/search/t?SEARCH='

# Read list of article titles from a CSV passed via cmd line arg
with open(input_file, 'rU') as f:
  reader = csv.reader(f, dialect=csv.excel_tab)
  articles = list(reader)

f = open(output_file, 'w')

# for every article, we need to do a bibliography lookup
for i, article in enumerate(articles):
  article_id = article[0].split(',')[0]
  title = article[0].split(',')[1].replace('||', ',')
  re.sub(r'[^\w]', ' ', title)
  if str(title) in invalid_title:
    print('Failed to read article: ' + article_id)
  else:
    req  = requests.get(tisch_old_url + title)
    data = req.text
    soup = BeautifulSoup(data)
    # TODO: Get this working
    # Right now we can't find "Result Item 1" and find returns none
    try:
      doc_id = soup.prettify().split('request~')[1].split('&')[0]
    except:
      doc_id = 'COULDNT FIND: ' + title
      print(soup.prettify())
    f.write(str(i) + ',' + doc_id + '\n') 

