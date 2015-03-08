Comp97
======

Senior Capstone Project

11/24/2014
Started writing scraper for ssl application. The web pages are poorly
structured with no class names or ids given for any of the fields in 
the table on each document page. To get the info for each page I just
look for things that only appear once in the html.

Skip a few months.....

1/30/2015
Scraper works right now. The dataset we are scraping lives on a 
server that can only be booted on a windows machine from a flash
drive. The server contains metadata on about 10,000 articles, and 
the articles can be accessed from a webpage where the only URL 
parameter we need to change is the article id, which is between
0 and 10,000. 

We changed the goal to be just getting the article title and the browse 
path (not authors or sources, since we will get that from tisch's api). 
The title will be used in the future to get extensive bibliographic 
info from the tischlibrary API. The browsepath will be used in the 
future to maintain the folder hierarchy used in the SSL. The output is 
a set of csv files containing the doc id, the title, and the browsepath, 
1000 docs to each file. This is currently working for 93% of articles, 
and the last 7% might just not exist. 

2/3/2015
Did some work on the bibliography lookup automater. Right now we can 
successfully read everything from the CSV output of scanssl (after 
doing a little cleanup to replace commas in the title field with ||)
and we can make a beautifulsoup soup instance from the tischlibrary 
search results page. What remains to be done is parsing the soup for
the first result and finding the unique document id that the tisch 
library system uses to store bibliography info. This is usually a
string in the format bXXXXXXX where the X's are numbers. Still 
digging through the html to find the right way to capture this id.

3/9/2015
Implemented MongoWriter.py, which uploads all of the data from a csv
file (tischdata) to a mongodb instance. NoSQL is ideal for our data
set because some of the records are from books, some are from journal
articles and other sources, and Tisch did not report the metadata in
a consistent format. So, to fit it all into a single relation we are
using MongoLab on Heroku (free for now).

We also need to figure out a way to represent the browsepath 
heirarchy in a mongo collection. 

I'm thinking 
bpath -> { folder: [bpath/subpath1, bpath/subpath2, ...], 
           files: [docid1, docid2, ...] }

And intermediary folders will just have an empty files array

Also implemented the first draft of a website, but it's in a new repo

Check out github.com/JakeSchmitz/SSL


