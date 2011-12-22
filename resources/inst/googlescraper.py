import feedparser, time, codecs
from readability.readability import Document
import urllib
from pyquery import PyQuery as pq


feedurls = {'Science' : 'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=snc&output=rss',
            'US' : 'http://news.google.com/news?ned=us&topic=n&output=rss',
            'World' : 'http://news.google.com/news?ned=us&topic=w&output=rss',
            'Politics' : 'http://news.google.com/news?q=politics&output=rss',
            'Business' : 'http://news.google.com/news?ned=us&topic=b&output=rss',
            'Tech' : 'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=tc&output=rss',
            'Sports' : 'http://news.google.com/news?ned=us&topic=s&output=rss',
            'Entertainment' : 'http://news.google.com/news?ned=us&topic=e&output=rss',
            'Health' : 'http://news.google.com/news?ned=us&topic=m&output=rss',
            'Top' : 'http://news.google.com/news?ned=us&topic=h&output=rss'
            }
article_ids = set()
root = '../datasets/news/'
sleeptime = 10


allbaseurls = set()
while True:
    for category, feedurl in feedurls.items():
        try:
            feed = feedparser.parse(feedurl)
        except Exception, e:
            print e, feedurl
            sleeptime *= 1.2
            continue
        sleeptime = 10
        for entry in feed.entries:
            article_id = entry.id
            article_link = entry.link
            link = article_link[article_link.find('&url=')+5:]
            allbaseurls.add(link[:link.find('/', 8)])
            if article_id in article_ids:
                print "skip", article_id
                continue

            try:
                html = urllib.urlopen(article_link).read()
                doc = Document(html)
                article_ids.add(article_id)
                title = doc.short_title()
                entry_texts = pq(doc.summary()).text()
                fname = '%s/%s/%s' % (root, category, article_id)
                f = codecs.open(fname, encoding='utf-8', mode='w')
                f.write(title)
                f.write('\n')
                f.write(entry_texts)
                f.close()
                print "write", title
                
            except Exception, e:
                print e
    time.sleep(sleeptime)

