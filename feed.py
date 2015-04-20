import time

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from splaysh.nut.models import *
from splaysh import settings
from splaysh.lib.feedparser import feedparser


def parse(nut_id, feed, parse_description=True):
    print nut_id
    now = time.localtime()
    me = User.objects.get(id=1)
    
    for e in feed.entries:
            nut = Nut.objects.get(id=nut_id)
            
            try:
                existing = Entry.objects.get(nut__id=nut.id, url=e.link)
                continue
            except ObjectDoesNotExist, d:
                pass
            
            description = ''
            if parse_description: 
                description = e.description
                
            nentry = Entry(user=me, 
                   nut=nut,
                   title = e.title,
                   content = description,
                   is_public = True,
                   url=e.link)
            nentry.save()    
    
            nentry.create_date = time.strftime('%Y-%m-%d %H:%M:%S', e.updated_parsed)
            nentry.save() 
            print e.title, e.link, nentry.create_date
            #print nentry.title, nentry.link, nentry.create_date
                
            

if __name__ == '__main__':
    feeds = [(settings.FAVNUT, "http://feeds.delicious.com/v2/rss/wbornor", False), 
    	     #settings.FAVNUT, "http://del.icio.us/rss/wbornor", False), 
             #(settings.CALNUT, "http://www.google.com/calendar/feeds/wbornor%40gmail.com/public/basic", True),
             (settings.VIDINUT, "http://www.youtube.com/rss/user/wbornor/videos.rss", True),
            ]
    
    for feed in feeds:
        parse(feed[0], feedparser.parse(feed[1]), feed[2])
    
