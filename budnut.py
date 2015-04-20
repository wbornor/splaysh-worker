from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from splaysh.nut.models import *
from splaysh.lib import minifb
from splaysh.lib import simplejson
from splaysh import settings



if __name__ == '__main__':
    _FbApiKey = ''
    _FbSecret = minifb.FacebookSecret('')
    auth_token=''
    
#    arguments = minifb.validate(_FbSecret, {"auth_token":auth_token})
#    auth_token = arguments["auth_token"]
#    print auth_token
#    
#    result = minifb.call("facebook.auth.getSession",
#                _FbApiKey, _FbSecret, auth_token=auth_token)
#    uid = result["uid"]
#    session_key = result["session_key"]
    uid = ''
    session_key = ''
    
    
#    users_info = minifb.call("facebook.users.getInfo",
#                    _FbApiKey, _FbSecret, session_key=session_key, fields="name", uids=uid)
#    print 'users_info', users_info
    
    friends_list = minifb.call("facebook.friends.get",
                    _FbApiKey, _FbSecret, session_key=session_key)
    #print 'friends_list', friends_list
    
    
    for fuid in friends_list:
        info = minifb.call("facebook.users.getInfo",
                    _FbApiKey, _FbSecret, session_key=session_key, fields="name,affiliations,pic", uids=fuid)
        
        info = info[0]
        underscore_name = info['name'].replace(' ', '_')
        url= "http://www.facebook.com/people/%s/%s" % (underscore_name, info['uid'])
        
        
        nut = Nut.objects.get(id=settings.BUDNUT)
        me = User.objects.get(id=1)
        now = datetime.now()
        #now = datetime.min
	#s = "1970-01-01T00:00:00"
	#from time import strptime
	#now = datetime(*strptime(s, "%Y-%m-%dT%H:%M:%S")[0:6])
        
        try:
            existing = Entry.objects.get(nut__id=settings.BUDNUT, url=url)
            continue
        except ObjectDoesNotExist, d:
            pass
        
        print 'users_info', info

        try:
            nentry = Entry(user=me, 
                           nut=nut,
                           title = "%s is now a Friend" % (info['name']),
			   content = ".",
                           is_public = True,
                           url=url)
            nentry.save()
            nentry.create_date = now
            nentry.save()
        except Exception, e:
            print e
            continue
        
        try:
            ndict = Dict(entry=nentry,
                         key='name',
                         value=info['name'])
            ndict.save()
        except Exception:
            pass
        
        try:
            ndict = Dict(entry=nentry,
                         key='uid',
                         value=info['uid'])
            ndict.save()
        except Exception:
            pass
        
        try:
            ndict = Dict(entry=nentry,
                         key='pic',
                         value=info['pic'])
            ndict.save()
        except Exception:
            pass
        
        try:
            ndict = Dict(entry=nentry,
                         key='affiliation_name',
                         value=info['affiliations'][0]['name'])
            ndict.save()
        except Exception:
            pass
        
        
        
