import os, sys, time
sys.path.append(os.path.join(os.getcwd(), '../..'))
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'splaysh.settings'
sys.path.pop()

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from splaysh.nut.models import *
from splaysh import settings
from splaysh.lib.feedparser import feedparser
#d = feedparser.parse("http://del.icio.us/rss/wbornor")
d = feedparser.parse("http://feeds.delicious.com/v2/rss/wbornor")


now = time.localtime()
me = User.objects.get(id=1)

for e in d.entries:
        try:
            nut = Nut.objects.get(pk=settings.FAVNUT)
            existing = Entry.objects.get(nut__id=nut.id, url=e.link)
            continue
        except ObjectDoesNotExist, d:
            pass
        
        try:
            nentry = Entry(user=me, 
                   nut=nut,
                   title = e.title,
                   is_public = True,
                   url=e.link)
            nentry.save()
    
            nentry.create_date = time.strftime('%Y-%m-%d %H:%M:%S', e.updated_parsed)
            nentry.save() 
            print e.title, e.link, nentry.create_date
            
        except Exception: pass

