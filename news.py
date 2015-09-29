import feedparser

yahoo = 'http://rss.dailynews.yahoo.co.jp/fc/domestic/rss.xml'

for entry in feedparser.parse(yahoo)['entries']:
    print(entry.title)
