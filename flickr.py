import time, hashlib
from datetime import datetime
import flickrapi, creds, persister

def download():

    flickr = flickrapi.FlickrAPI(creds.flickr["api_key"])
    photos = flickr.walk(user_id=creds.flickr["user_id"],
            min_taken_date='2008-08-20') #todo - fix min_taken_date
    return photos


def getThumbnailUrl(server_id, photo_id, secret):
    #docs: https://www.flickr.com/services/api/misc.urls.html
    farm_id = 1
    size_suffix = 'n'
    return 'https://farm%s.staticflickr.com/%s/%s_%s_%s.jpg' % farm_id, server_id, photo_id, secret, size_suffix

def transform(photos):
    entries = []
    for photo in photos:
        print photo.get('title')
        created = photo.get('datetaken') or datetime.now() #todo - is datetake a real attribute?
        entry = {
            'nut_id': 3,
            'nut_type': 'PHOTONUT',
            'create_date': str(created),
            'is_photoset': False,
            'content': photo.get('id'),
            'is_public': photo.get('ispublic'),
            'thumb_url': getThumbnailUrl(photo.get('server'), photo.get('id'), photo.get('secret')),
            'url': 'https://www.flickr.com/photos/%s/%s' % (creds.flickr["user_id"], photo.get('id')),
            'title': photo.get('title')
        }

        entry["id"] = 'talknut.' + hashlib.sha256(entry['url']).hexdigest()

        entry['flickr::photo'] = str(photo) #todo verify this actually works

        entries.append(entry)
    return entries

def main():
    photos = download()
    json = transform(photos)
    persister.put(json)

    print "done"

def handler(event, context):
    main()

if __name__ == '__main__':
    main()
