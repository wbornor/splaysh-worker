import os, sys, time, datetime
sys.path.append(os.path.join(os.getcwd(), '../..'))
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'splaysh.settings'
sys.path.pop()

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from splaysh.nut.models import *
from splaysh import settings
from splaysh.lib.pyaws import ecs

def insert_media(asin=None, query=None, create_date=None):
    if not create_date:
        now = datetime.datetime.now()
    else:
        now = create_date 
        
    me = User.objects.get(id=1)
    
    try:
        ecs.setLicenseKey(settings.ECS_LICENSE_KEY)
        r = ecs.ItemLookup(asin, ResponseGroup='ItemAttributes,Images,Large')
        
        for item in r:
                if hasattr(item, 'Author'):
                    if isinstance(item.Author, list): 
                        author = item.Author[0]
                    else:
                        author = item.Author
                        
                    title = '%s by %s' % (item.Title, author)
                else:
                    title = '%s' % (item.Title)
                img_url = item.MediumImage.URL
                item_url = item.DetailPageURL
                editorial_review = "";
                
	        if isinstance(item.EditorialReviews.EditorialReview,list):
			editorial_review = item.EditorialReviews.EditorialReview[0].Content
	        else:
			editorial_review = item.EditorialReviews.EditorialReview.Content
	
                try:
                    existing = Entry.objects.get(nut__id=settings.MEDIANUT, url=item_url)
                    continue
                except ObjectDoesNotExist, d:
                    pass
                
		nut = Nut.objects.get(pk=settings.MEDIANUT)
                nentry = Entry(user=me, 
                       nut=nut,
                       title = title,
                       content = """<table border="0">
                                           <tr valign="top">
                                               <td>
                                                   <a href="%s"><img style="float:left;margin-right:5px;" src="%s" border="0"/></a>
                                               %s</td>
                                           </tr>
                                       </table>"""  % (item_url, img_url, editorial_review),
                       is_public = True,
                       url=item_url)
                nentry.save()
                nentry.create_date = now
                nentry.save() 
                print asin, title, now
                
    except Exception, e: print e
    
if __name__ == '__main__':
    entries = Entry.objects.filter(nut__id=5)
    for entry in entries:
        start = entry.content.index('ASIN=')+5
        end = entry.content.index('%', start)
        asin = entry.content[start:end]
        insert_media(asin=asin, create_date=entry.create_date)
        
