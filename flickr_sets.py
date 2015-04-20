import os, sys, time
sys.path.append(os.path.join(os.getcwd(), '../..'))
sys.path.append(os.getcwd())
sys.path.append('/home/wbornor/webapps/django/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'splaysh.settings'
os.environ['PYTHONPATH'] = '/home/wbornor/webapps/django/'
sys.path.pop()

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from splaysh.nut.models import *
from splaysh import settings
from splaysh.lib import flickrapi

now = time.localtime()
me = User.objects.get(id=1)


f = flickrapi.FlickrAPI(settings.flickr_api_key, settings.flickr_api_secret)

r = f.photosets_getList(user_id=settings.flickr_user_id)
nut = Nut.objects.get(id=settings.PHOTONUT)

for set in r.photosets[0].photoset:
        try:
            existing = Entry.objects.get(nut__id=3, url="http://www.flickr.com/photos/weslaaaaay/sets/%s/" % (set['id']))
            continue
        except ObjectDoesNotExist, d:
            pass
        
        date_taken = f.photosets_getPhotos(photoset_id=set['id'], extras='date_taken').photoset[0].photo[0]['datetaken']
        print set.title[0].elementText, set['id'], date_taken
        nentry = Entry(user=me, 
                       nut=nut,
                       title = set.title[0].elementText,
                       content = set['id'],
                       is_public = True,
                       url="http://www.flickr.com/photos/weslaaaaay/sets/%s/" % (set['id']))
        nentry.save()
        nentry.create_date = date_taken
        nentry.save()
