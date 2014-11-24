# I haven't tested this at all yet!!!!!
import sys
import urllib.request


class doc:
  def __init__(self, doc_id, title, authors, source):
    self.doc_id = doc_id
    self.title = title
    self.authors = authors
    self.source = source

  def to_csv(self, delim=','):
    str(self.doc_id) + delim + self.title + delim + self.authors + delim + self.source

base_url = 'http://127.0.0.1:1025/gsdl?a=d&d=D'
# articles is a map from doc ids to an instance of a doc 
# class
articles = []

for i in range(9999):
  page = urllib.request.urlopen(base_url + str(i)).read().decode('utf-8')
  # the title is in the only h3 tag
  chunks = page.split('h3>')
  # remove part of closing h3 tag from title
  title = chunks[1].replace('</', '')
  print(title)
  # Read the html of one of the pages and this will make sense
  # It would be cleaner if people knew how to use ids in html
  auts = chunks[-1].split('Author(s)</td>')[0].split('<td bgcolor="#E6F0FF">')[0].split('</td>')[0]
  src = chunks[-1].split('Source</td>')[0].split('<td bgcolor="#E6F0FF">')[0].split('</td>')[0]
  article = doc(i, title, auts, src)
  print(article.to_csv())
  articles.append(article)
  # Check if this article already has a valid link/ source
  #if chunks[-1].find('[Article not available]') >= 0:
    # This article does not have a source available
    #print doc.to_csv() 
  
