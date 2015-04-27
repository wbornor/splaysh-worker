import os, sys, time
from datetime import datetime

import urllib
import uuid
import tweepy
import simplejson
import boto
from boto.s3.connection import S3Connection
import creds


def download():
    auth = tweepy.OAuthHandler(creds.twitter["consumer_key"], creds.twitter["consumer_secret"])
    auth.set_access_token(creds.twitter["access_token"], creds.twitter["access_token_secret"])

    api = tweepy.API(auth)

    # TODO only download latest tweets
    tweets = api.user_timeline()
    return tweets

# transform a list of tweets into splayshdb-json
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
            'create_date': str(created),
            'content': tweet.text,
            'is_public': 1,
            'url': 'https://twitter.com/wbornor/status/%s' % tweet.id_str,
        }
        if 'media' in tweet.entities:
            entry['twitter_media'] = tweet.entities['media']

        entries.append(entry)
    return simplejson.dumps(entries)


def persist(json):
    s3 = S3Connection(creds.aws["aws_access_key_id"], creds.aws["aws_secret_access_key"])
    from boto.s3.key import Key

    bucket = s3.get_bucket("splaysh.com")
    k = Key(bucket)
    k.key = 'splayshdb-test.js'
    print k.get_contents_as_string()


def main():
    now = time.localtime()

    tweets = download()
    json = transform(tweets)

    #TODO put json to S3
    #persist(json)

    print "done"


if __name__ == '__main__':
    main()