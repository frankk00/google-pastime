import urllib
from datetime import datetime

from page import Page
from meta import Session

search = '#hashtag'
urlparam = urllib.urlencode({'q':search})
initURL = u'http://www.google.com/search?tbm=mbl&hl=en&source=hp&biw=1362&bih=651&' + \
          urlparam + u'&aq=f&aqi=&aql=&oq=#sclient=psy&hl=en&source=hp&' + \
          urlparam + u'&aq=f&aqi=g-s1g-sx4&oq=&pbx=1&tbm=mbl:1&' + \
          u'tbs=mbl:1,mbl_hs:1307059378,mbl_he:1307145778,mbl_rs:1307070778,mbl_re:1307102578,mbl_dr:o' + \
          u'&fp=e3968b5bcabb7a70&biw=1362&bih=651'

selector = 'ol#rso'
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91 Safari/534.30'
referer = initURL

page = Page('url', 'html', datetime.now(), 'oldurl', 'newurl')
Session.add(page)
Session.commit()
print Session.query(Page).count()
