import time

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from splaysh.nut.models import *
from splaysh import settings
from splaysh.lib.pyaws import ecs

now = time.localtime()
me = User.objects.get(id=1)
nut = Nut.objects.get(pk=settings.WISHNUT)

ecs.setLicenseKey('')

r = ecs.ListLookup('WishList', '', ResponseGroup='ListFull,Images,Large', AWSAccessKeyId='')

l = r[0]
for li in l.ListItem:
        date = li.DateAdded
        title = li.Item.Title
        img_url = li.Item.MediumImage.URL
        item_url = li.Item.DetailPageURL
        editorial_review = "";
        try:
            if isinstance(li.Item.EditorialReviews.EditorialReview,list):
                editorial_review = li.Item.EditorialReviews.EditorialReview[0].Content
            else:
                editorial_review = li.Item.EditorialReviews.EditorialReview.Content
        except Exception:
            pass
        
        
        
        try:
            existing = Entry.objects.get(nut__id=nut.id, url=item_url)
            continue
        except ObjectDoesNotExist, d:
            pass
        
        print title, date
        
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

        nentry.create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date, '%Y-%m-%d'))
        nentry.save() 

