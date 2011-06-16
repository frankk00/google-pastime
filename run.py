import re
import time
import urllib
import urllib2
from lxml import etree
from lxml.cssselect import CSSSelector
from datetime import datetime
from sqlalchemy import desc

from page import Page
from meta import Session

search = '#hashtag'
urlparam = urllib.urlencode({'q':search})

initURL = u'http://www.google.com/search?hl=en&source=hp&biw=1362&bih=651&' + urlparam + u'&aq=f&aqi=&oq=&&tbm=mbl:1&tbs=mbl:1,mbl_hs:1307059378,mbl_he:1307145778,mbl_rs:1307070778,mbl_re:1307102578,mbl_dr:o'

begintime = datetime.strptime('Jun 3, 2011', '%b %d, %Y')
endtime = datetime.strptime('Jun 7, 2011', '%b %d, %Y')

useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91 Safari/534.30'

page = Session.query(Page).order_by(desc(Page.id)).first()
if page:
    url = page.newerurl
    lasturl = page.url
else:
    url = initURL
    lasturl = ''

while True:
    req = urllib2.Request(url)
    req.add_header("User-Agent", useragent)
    if lasturl:
        req.add_header('Referer', lasturl)
    html = unicode(urllib2.urlopen(req).read(), errors='ignore')
    doc = etree.HTML(html)
    rtr = CSSSelector('ol#rtr')(doc)
    if rtr:
        numresults = len(rtr[0].getchildren())
    else:
        numresults = 0
    print 'hit ' + url + ' got ' + str(numresults) + ' results'
    rhscol = CSSSelector('div#rhscol')(doc)[0]
    links = [a for a in rhscol.getiterator('a')]
    if len(links) != 3 or 'Older' not in links[1].text or 'Newer' not in links[2].text:
        print 'Cant find older and newer links here, backing up'
        oldurl = page.url
        match = re.search('mbl_hs:(\d+),mbl_he:(\d+),mbl_rs:(\d+),mbl_re:(\d+)', oldurl)
        mbl_hs = int(match.group(1)) + 600
        mbl_he = int(match.group(2)) + 600
        mbl_rs = int(match.group(3)) + 600
        mbl_re = int(match.group(4)) + 600
        url = oldurl.replace(match.group(0), 'mbl_hs:'+str(mbl_hs)+',mbl_he:'+str(mbl_he)+',mbl_rs:'+str(mbl_rs)+',mbl_re:'+str(mbl_re))
        lasturl = oldurl
        time.sleep(10)
        continue
    olderurl = u'http://www.google.com' + links[1].attrib['href']
    newerurl = u'http://www.google.com' + links[2].attrib['href']
    page = Page(url, html, numresults, olderurl, newerurl)
    Session.add(page)
    Session.commit()
    lasturl = url
    url = newerurl
    for rtdm in CSSSelector('span.rtdm')(doc):
        td, date = [text for text in rtdm.itertext()]
        day = datetime.strptime(date, '%b %d, %Y')
        if day > endtime:
            print 'Quitting, ' + str(day) + ' > ' + str(endtime)
            exit()
    time.sleep(10)
