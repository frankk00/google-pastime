import lxml.html as lxml
from lxml.cssselect import CSSSelector

from page import Page
from tweet import Tweet
from meta import Session

numdupes = 0
for page in Session.query(Page).order_by(Page.id):
    doc = lxml.document_fromstring(page.html)
    rtr = CSSSelector('ol#rtr')(doc)
    if not rtr:
        continue
    for tweet in rtr[0].getchildren():
        twitterlink = CSSSelector('span.a')(tweet)
        assert len(twitterlink) == 1 and twitterlink[0].text == 'Twitter'
        toclear = []
        c = twitterlink[0]
        while c is not None:
            toclear.append(c)
            c = c.getnext()
        for c in toclear:
            c.clear()
        text = lxml.tostring(tweet, encoding=unicode, method='text')
        t = Tweet(text)
        if Session.query(Tweet).filter(Tweet.md5==t.md5).first() is None:
            Session.add(t)
        else:
            numdupes = numdupes + 1
    
Session.commit()
print 'committed, there were ' + str(numdupes) + ' dupes'
