import os, sys, time
#os.environ['DJANGO_SETTINGS_MODULE'] = 'splaysh.settings'

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from splaysh.nut.models import *
from splaysh import settings
from splaysh.lib.feedparser import feedparser
d = feedparser.parse("http://rss.netflix.com/TrackingRSS?id=P6696698795577717536481904413749894")


now = time.localtime()
me = User.objects.get(id=1)

for e in d.entries:
        try:
            nut = Nut.objects.get(pk=settings.MEDIANUT)
            existing = Entry.objects.get(nut__id=nut.id, url=e.link)
            continue
        except ObjectDoesNotExist, d:
            pass
        
        try:
	    print e.title
	    if not e.title.startswith('Shipped: '):
		continue
	    
	    e.title = e.title[9:]

            nentry = Entry(user=me, 
                   nut=nut,
                   title = e.title,
		   content = e.description,
                   is_public = True,
                   url=e.link)
            nentry.save()
    
            #nentry.create_date = time.strftime('%Y-%m-%d %H:%M:%S', e.updated_parsed)
            #nentry.save() 
	    ndict = Dict(entry=nentry,
			key="icon_url",
			value="/img/netflix-logo.gif")
	    ndict.save()

            print e.title, e.link, nentry.create_date
            
        except Exception, e: print e

