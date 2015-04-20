import os, sys, time

sys.path.append(os.path.join(os.getcwd(), '../..'))
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'splaysh.settings'
sys.path.pop()

from splaysh import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from splaysh.nut.models import *

import urllib
from splaysh.lib import simplejson as json

def parse(nut_id, url, user):
    print(nut_id)
    now = time.localtime()
    me = User.objects.get(id=1)
    
    response = urllib.urlopen(url)
    html = response.read()
    results = json.loads(html)['results']

    for r in results:
            nut = Nut.objects.get(id=nut_id)
            
            id = r['id']
            tweetUrl = 'http://twitter.com/#!/'+user+'/status/'+str(id)

            try:
                existing = Entry.objects.get(nut__id=nut.id, url=tweetUrl)
                continue
            except ObjectDoesNotExist, d:
                pass
            
            nentry = Entry(user=me, 
                   nut=nut,
                   title = '@'+user,
                   content = r['text'],
                   is_public = True,
                   url=tweetUrl)
            nentry.save()    
    
            nentry.create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            #nentry.save() 
            print(user, id, tweetUrl, r['text'], r['created_at'])
                
            

if __name__ == '__main__':
    feeds = [(settings.ANALNUT, 'http://search.twitter.com/search.json?q=from%3Aanalnut', 'analnut'), 
            ]
    
    for feed in feeds:
        parse(feed[0], feed[1], feed[2])
    
