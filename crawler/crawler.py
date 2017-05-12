#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import pyodbc
import sys
import time
import urllib2

def connect():
    try:
        # On MacOS
        return pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:centaurus-db.database.windows.net,1433;\
            Database=centaurus;Uid=centaurus@centaurus-db;Pwd=k9Rjm7g8V7dh;Encrypt=yes;Connection Timeout=90;')
    except pyodbc.Error as e:
        try:
            # On Ubuntu
            return pyodbc.connect('DSN=centaurusdatasource;Database=centaurus;Uid=centaurus@centaurus-db;Pwd=k9Rjm7g8V7dh;Encrypt=yes;Connection Timeout=90;')
        except Exception as e:
            # On Windows
            return pyodbc.connect('Driver={SQL Server};Server=tcp:centaurus-db.database.windows.net,1433;\
                Database=centaurus;Uid=centaurus@centaurus-db;Pwd=k9Rjm7g8V7dh;Encrypt=yes;Connection Timeout=90;')


datadict = []
year = int(sys.argv[1])
month = int(sys.argv[2])
start = int(sys.argv[3])
ends = int(sys.argv[4])
delay = 1
if len(sys.argv) > 4:
    delay = int(sys.argv[5])

for index in range(start, ends):
    time.sleep(delay)

    url = "https://arxiv.org/abs/%s%s.%s" % (str(year),str(month).zfill(2), str(index).zfill(5))
    while True:
        try:
            site = urlopen(url)
            conn = connect()
            cur = conn.cursor()
            break
        except urllib2.HTTPError as e:
            print "!!! BLOCKED !!!\nFix connection and run: python crawler.py %s %s %s %s %s" % (str(year),str(month),index, ends, delay)
            conn.close()
            time.sleep(60)
    if site.getcode() >= 200 and site.getcode() <= 400:
        page = site.read()
        soup = BeautifulSoup(page, "html5lib")

        title = soup.select("h1.title.mathjax")[0].getText()
        title = title.split("Title:\n")[1]

        authors_text = soup.find_all("div", class_="authors")[0].find_all("a")
        authors = []
        authors_id = []
        for au in authors_text:
            author_name = au.getText()
            authors.append(au.getText())
            cur.execute('select id from author where name like ?', au.getText())
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    authors_id.append(row.id)
            else:
                cur.execute('insert into author (name) output Inserted.id values (?)', author_name)
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        authors_id.append(row.id)
        authors_string = ",".join(authors)

        abstract = soup.select("blockquote.abstract.mathjax")[0].getText()
        abstract = abstract.split("Abstract: ")[1]
        data_id = None
        try:
            cur.execute('insert into data (title, authors,abstract,url, year, month) output Inserted.id values (?,?,?,?,?,?)', title, authors_string, abstract, url, str(year), str(month))
            row = cur.fetchone()
            if row:
                data_id = row.id
            else:
                data_id = None
            print "[NEW %s] %s -> %s" % (data_id, url, title)
        except pyodbc.IntegrityError as e:
            print "[EXISTING] %s -> %s" % (url, title)

        for author_id in authors_id:
            if data_id is not None:
                try:
                    cur.execute('insert into author_data (data_id, author_id) values (?,?)', data_id, author_id)
                except pyodbc.IntegrityError as e:
                    print "[ERROR] REPEATING AUTHOR"
        conn.commit()
        conn.close()
    else:
        print "[ERROR] %s -> Got Error [%s]" % (url, site.getcode())

print "Bye!"

