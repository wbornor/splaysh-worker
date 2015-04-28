import time
from datetime import datetime

import uuid
import tweepy
import simplejson
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError
import creds


def download():
    auth = tweepy.OAuthHandler(creds.twitter["consumer_key"], creds.twitter["consumer_secret"])
    auth.set_access_token(creds.twitter["access_token"], creds.twitter["access_token_secret"])

    api = tweepy.API(auth)

    # TODO only download latest tweets
    tweets = api.user_timeline()
    return tweets

# transform -   transform a list of tweets into splayshdb-json
'''
Example splayshdb-json format
[
    {
        "id" : 3233,
        "nut_id" : 2,
        "create_date" : "2013-03-24 05:57:01",
        "title" : "Flickr: The KAP rigs Pool",
        "content" : "",
        "is_public" : 1,
        "url" : "http://www.flickr.com/groups/kaprigs/pool/with/8061790889/#photo_8061790889"
    },
]
'''


def transform(tweets):
    entries = []
    for tweet in tweets:
        print tweet.text
        created = tweet.created_at or datetime.now()
        entry = {
            'id': str(uuid.uuid4()),
            'nut_id': 1,
            'nut_type': 'TALKNUT',
            'create_date': str(created),
            'content': tweet.text,
            'is_public': 1,
            'url': 'https://twitter.com/wbornor/status/%s' % tweet.id_str,
        }

        for e in tweet.entities:
            entry['tweet::entities::' + e] = tweet.entities[e]

        entry['tweet::id_str'] = tweet.id_str
        entry['tweet::created_at'] = str(tweet.created_at)
        entry['tweet::author::id_str'] = tweet.author.id_str
        entry['tweet::author::screen_name'] = tweet.author.screen_name
        entry['tweet::author::name'] = tweet.author.name
        entry['tweet::author::profile_image_url_https'] = tweet.author.profile_image_url_https

        entries.append(entry)
    return entries


def persist(json):
    s3 = S3Connection(creds.aws["aws_access_key_id"], creds.aws["aws_secret_access_key"])

    # TODO - map out directory layout
    # s3://splaysh.com/splayshdb/head.json # head - lists past n entries
    # s3://splaysh.com/splayshdb/talknut/ # head - lists past n talknut entries
    # s3://splaysh.com/splayshdb/talknut/2015/ # lists all talknut entries in 2015
    # s3://splaysh.com/splayshdb/talknut/2015/2015-04-27.json # many files YYYY-MM-DD.json
    # s3://splaysh.com/splayshdb/budnut/
    # s3://splaysh.com/splayshdb/budnut/2015/
    bucket = s3.get_bucket("splaysh.com")

    #TODO - write to head file

    #overwrite talknut head file
    k = Key(bucket)
    k.key = 'splayshdb/talknut/head.json'
    try:
        head = simplejson.loads(k.get_contents_as_string())
    except S3ResponseError:
        # head is missing
        head = []

    #TODO - only write on change

    k.set_contents_from_string(simplejson.dumps(json))

    #TODO - overwrite talknut year files

def main():
    now = time.localtime()

    tweets = download()
    json = transform(tweets)
    persist(json)

    print "done"


if __name__ == '__main__':
    main()