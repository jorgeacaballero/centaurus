from bs4 import BeautifulSoup

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.error import URLError
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib2 import URLError
    from urllib2 import HTTPError

try:
    # For Python 3.0 and later
    from urllib.parse import urlparse
except ImportError:
    # Fall back to Python 2's urlparse
    from urlparse import urlparse

try:
    from simplejson import loads, dumps
except ImportError:
    from json import loads, dumps

import psycopg2

try:
    conn = psycopg2.connect("dbname='centaurus' host='localhost'")
except:
    print "I am unable to connect to the database"

datadict = []
year = 17
month = 1
start = 11
ends = 20
for index in range(start, ends):
    url = "https://arxiv.org/abs/%s%s.%s" % (str(year),str(month).zfill(2), str(index).zfill(5))
    site = urlopen(url)
    if site.getcode() >= 200 and site.getcode() <= 400:
        page = site.read()
        soup = BeautifulSoup(page, "html5lib")

        title = soup.select("h1.title.mathjax")[0].getText()
        title = title.split("Title:\n")[1]

        authors_text = soup.find_all("div", class_="authors")[0].find_all("a")
        authors = []
        for au in authors_text:
            authors.append(au.getText())
        authors_string = ",".join(authors)

        abstract = soup.select("blockquote.abstract.mathjax")[0].getText()
        abstract = abstract.split("Abstract: ")[1]

        print "%s -> %s" % (url, title)
        datadict.append({"title": title, "authors": authors_string, "abstract": abstract, "url": url, "year": year, "month": month})
    else:
        print "%s -> [%s] %s" % (url, site.getcode(), "Error, continuing...")


datadict = tuple(datadict)
cur = conn.cursor()
cur.executemany("""insert into data (title,authors,abstract,url, year, month) values (%(title)s, %(authors)s, %(abstract)s, %(url)s, %(year)s, %(month)s) on conflict (url) do nothing""", datadict)


conn.commit()
conn.close()
print "Bye!"