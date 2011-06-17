import csv
import unicodedata

from tweet import Tweet
from meta import Session

writer = csv.writer(open('tweets.csv', 'wb'), dialect='excel')
for tweet in Session.query(Tweet):
    text = unicodedata.normalize('NFKD', tweet.text).encode('ascii', 'ignore')
    writer.writerow([text])
