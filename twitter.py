import os, sys, time

import urllib
import tweepy
import simplejson
import boto
from boto.s3.connection import S3Connection
import creds

def download():
    auth = tweepy.OAuthHandler(creds.twitter["consumer_key"], creds.twitter["consumer_secret"])
    auth.set_access_token(creds.twitter["access_token"], creds.twitter["access_token_secret"])

    api = tweepy.API(auth)

    tweets = api.user_timeline()
    for tweet in tweets:
        print tweet.text

def persist(json):
    s3 = S3Connection(creds.aws["aws_access_key_id"], creds.aws["aws_secret_access_key"])
    from boto.s3.key import Key
    bucket = s3.get_bucket("splaysh.com")
    k = Key(bucket)
    k.key = 'splayshdb-test.js'
    print k.get_contents_as_string()

def main():
    now = time.localtime()

    #TODO get payload from service
    download()
    #response = urllib.urlopen(url)
    #html = response.read()
    #results = simplejson.loads(html)['results']

    #TODO transform json
    #simplejson.

    #TODO put json to S3

    #persist('hi')

    print "done"

if __name__ == '__main__':
    main()