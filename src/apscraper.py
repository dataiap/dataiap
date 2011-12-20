import feedparser, time, codecs
from pyquery import PyQuery as pq


feedurls = {'Science' : 'http://hosted2.ap.org/atom/APDEFAULT/b2f0ca3a594644ee9e50a8ec4ce2d6de',
            'US' : 'http://hosted2.ap.org/atom/APDEFAULT/386c25518f464186bf7a2ac026580ce7',
            'World' : 'http://hosted2.ap.org/atom/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5',
            'Politics' : 'http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa',
            'Business' : 'http://hosted2.ap.org/atom/APDEFAULT/f70471f764144b2fab526d39972d37b3',
            'Tech' : 'http://hosted2.ap.org/atom/APDEFAULT/495d344a0d10421e9baa8ee77029cfbd',
            'Sports' : 'http://hosted2.ap.org/atom/APDEFAULT/347875155d53465d95cec892aeb06419',
            'Entertainment' : 'http://hosted2.ap.org/atom/APDEFAULT/4e67281c3f754d0696fbfdee0f3f1469',
            'Health' : 'http://hosted2.ap.org/atom/APDEFAULT/bbd825583c8542898e6fa7d440b9febc',
            'Strange' : 'http://hosted2.ap.org/atom/APDEFAULT/aa9398e6757a46fa93ed5dea7bd3729e',
            'Top' : 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305'}
article_ids = set()
root = '../datasets/news/'
sleeptime = 10


while True:
    for category, feedurl in feedurls.items():
        feed = feedparser.parse(feedurl)
        for entry in feed.entries:
            article_id = entry.id
            article_link = entry.link

            if article_id in article_ids:
                print "skip", article_id
                continue
            d = pq(article_link)
            try:
                article_ids.add(article_id)
                title = d(".entry-title")[0].text_content()
                title.replace('\n', '')
                econts = d(".entry-content")
                entry_texts = map(lambda econt: econt.text_content(), econts)
                fname = '%s/%s/%s' % (root, category, article_id)
                f = codecs.open(fname, encoding='utf-8', mode='w')
                f.write(title)
                f.write('\n')
                for text in entry_texts:
                    f.write(text)
                f.close()
                print "write", title
                
            except Exception, e:
                print e
    time.sleep(sleeptime)




