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


site = urlopen("https://arxiv.org/abs/1009.0001").getcode()
if site.getcode() >= 200 and site.getcode() <= 400:
    page = site.read()
    soup = BeautifulSoup(page, "html5lib")
    print soup