# I haven't tested this at all yet!!!!!
# But it did produce the output I needed, and I don't need to repurpose it, soooo.....
import sys
import urllib.request
import math
import re

# A Doc is a document in the SSL database from the flashdrive we got from GDAE
class Doc:
  def __init__(self, doc_id, title, authors, source, url, bpath):
    self.doc_id = doc_id
    self.title = '\"' + str(title.replace(u"\u2018", "'").replace(u"\u2019", "'")) + '\"'
    self.authors = '\"' + str(authors.replace(u"\u2018", "'").replace(u"\u2019", "'")) + '\"'
    self.source = source
    self.browsepath = '\"' + '/'.join(bpath) + '\"'
    if url == None:
      url = 'None';
    self.link = url

  def to_csv(self, delim=','):
    # Here is an alternate way to print the article 
    # return str(self.doc_id) + delim + str(self.title) + delim + str(self.authors) + delim + str(self.source) + delim + self.link + '\n'
    return str(self.doc_id) + delim + str(self.title) + delim + str(self.browsepath) + '\n'    

base_url = 'http://127.0.0.1:1025/gsdl?a=d&d=D'
# articles is a map from doc ids to an instance of a doc 
# class
articles = []
# Break files up into 1000 row chunks
file_base = 'scraped'

for i in range(6000, 9999):
  page = urllib.request.urlopen(base_url + str(i)).read().decode('utf-8')
  # the title is in the only h3 tag
  chunks = page.split('h3>')
  # remove part of closing h3 tag from title
  try:
    title = chunks[1].replace('</', '')
  except:
    title = scraping_error
  # Read the html of one of the pages and this will make sense
  # It would be cleaner if people knew how to use ids in html
  scrape_error = 'SCRAPING ERROR'
  try: 
    auts = chunks[-1].split('Author(s)</td>')[1].split('<td bgcolor="#E6F0FF">')[1].split('</td>')[0]
  except:
    auts = scrape_error
  try:
    src = chunks[-1].split('Source</td>')[1].split('<td bgcolor="#E6F0FF">')[1].split('</td>')[0]
  except:
    src = scrape_error
  try:
    art = chunks[-1].split('<td valign="top">Article</td>')[1].split('<td bgcolor="#E6F0FF" colspan="3">')[1].split('</td>')[0]
  except:
    art = scrape_error
  # Browse Path is the most complicated to parse because each part of the path is on a separate line 
  # and there is a lot of ascii used to format the browsepath within the html table cell
  try:
    browsepath_html= chunks[-1].split('Browse Path(s)')[1]
    browsepath = browsepath_html.split('<td bgcolor="#E6F0FF">')[1].split('</td>')[0].replace('-', '').strip().split('<br/>')
    if len(browsepath[-1].strip()) == 0 and len(browsepath) > 1:
      browsepath.pop()
    browespath = map(lambda x: x.strip().replace(u"\u2018", "'").replace(u"\u2019", "'"), browsepath)
  except:
    browsepath = scrape_error
  article = Doc(i, title, auts, src, art, browsepath)
  # write to a different file every 1000 documents 
  # needed to do this because my VM crashed frequently
  if i % 1000 == 0:
    print('Finished ' + str(i) + ' articles')
    fname = file_base + str(i) + '-' + str(i + 999) + '.csv'
    f = open(fname, 'w')
  if article.title != None:
    try:
      f.write(article.to_csv())
      #print(article.to_csv())
    except:
      # log write failures to stdout
      print('Failed on article: ' + str(i))
      print(article.to_csv())
  

