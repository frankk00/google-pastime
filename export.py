import csv
import unicodedata

from tweet import Tweet
from meta import Session

writer = csv.writer(open('tweets.csv', 'wb'), dialect='excel')
for tweet in Session.query(Tweet).order_by(Tweet.when):
    text = unicodedata.normalize('NFKD', tweet.text).encode('ascii', 'ignore')
    date = tweet.when.strftime('%m/%d/%Y %I:%M:%S %p')
    writer.writerow([text, date])
