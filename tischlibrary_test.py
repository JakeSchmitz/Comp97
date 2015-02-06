"""This tests the scraping of JSON search results from the Tisch Library website."""

import requests

c = {}
c['Summon-Two'] = 'TRUE'
c['__utma'] = '160199096.1776388197.1421705704.1423013448.1423184948.4'
c['__utmc'] = '160199096'
c['__utmz'] = '160199096.1423184948.4.4.utmcsr=tischlibrary.tufts.edu|utmccn=(referral)|utmcmd=referral|utmcct=/'
#c['hasSavedItems'] = 1

r = requests.get('http://tufts.summon.serialssolutions.com/api/search?pn=1&ho=t&q=The+Localization+of+Development+in+Comparative+Perspective', cookies=c)

print r.text
