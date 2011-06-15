import time
import urllib
import urllib2
from lxml import etree
from lxml.cssselect import CSSSelector
from datetime import datetime

from page import Page
from meta import Session

search = '#hashtag'
urlparam = urllib.urlencode({'q':search})

initURL = u'http://www.google.com/search?hl=en&source=hp&biw=1362&bih=651&' + urlparam + u'&aq=f&aqi=&oq=&&tbm=mbl:1&tbs=mbl:1,mbl_hs:1307059378,mbl_he:1307145778,mbl_rs:1307070778,mbl_re:1307102578,mbl_dr:o'

useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91 Safari/534.30'

url = initURL
lasturl = ''
while True:
    req = urllib2.Request(url)
    req.add_header("User-Agent", useragent)
    if lasturl:
        req.add_header('Referer', lasturl)
    print 'hitting ' + url
    html = unicode(urllib2.urlopen(req).read(), errors='ignore')
    doc = etree.HTML(html)
    rtr = CSSSelector('ol#rtr')(doc)
    if rtr:
        numresults = len(rtr[0].getchildren()))
    else:
        numresults = 0
    rhscol = CSSSelector('div#rhscol')(doc)[0]
    links = [a for a in rhscol.getiterator('a')]
    assert 'Older' in links[1].text
    assert 'Newer' in links[2].text
    olderurl = u'http://www.google.com' + links[1].attrib['href']
    newerurl = u'http://www.google.com' + links[2].attrib['href']
    page = Page(url, html, numresults, olderurl, newerurl)
    Session.add(page)
    Session.commit()
    url = newerurl
    time.sleep(10)
