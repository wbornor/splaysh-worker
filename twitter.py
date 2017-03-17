__author__ = 'wesbornor'

from datetime import datetime

import hashlib
import tweepy
import simplejson

import creds, persister

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
        print "tweet.text: " + tweet.text
        created = tweet.created_at or datetime.now()
        entry = {
            'nut_id': 1,
            'nut_type': 'TALKNUT',
            'create_date': str(created),
            'content': tweet.text,
            'is_public': 1,
            'url': 'https://twitter.com/wbornor/status/%s' % tweet.id_str,
            'title': '@wbornor',
        }
        entry["id"] = 'talknut.' + hashlib.sha256(entry['url']+entry['create_date']).hexdigest()

        entry['tweet::json'] = simplejson.dumps(tweet._json)

        for e in tweet.entities:
            if tweet.entities[e]:
                try :
                    entry['tweet::entities::' + e] = simplejson.dumps(tweet.entities[e])
                except :
                    print('simplejson fail:' + tweet.entities[e])

        if tweet.id_str:
            entry['tweet::id_str'] = tweet.id_str

        if tweet.created_at:
            entry['tweet::created_at'] = str(tweet.created_at)

        if tweet.author and tweet.author.id_str:
            entry['tweet::author::id_str'] = tweet.author.id_str

        if tweet.author and tweet.author.screen_name:
            entry['tweet::author::screen_name'] = tweet.author.screen_name

        if tweet.author and tweet.author.name:
            entry['tweet::author::name'] = tweet.author.name

        if tweet.author and tweet.author.profile_image_url_https:
            entry['tweet::author::profile_image_url_https'] = tweet.author.profile_image_url_https

        entries.append(entry)

    return entries

def main():
    tweets = download()
    json = transform(tweets)
    persister.put(json)

    print "done"

def handler(event, context):
    main()

if __name__ == '__main__':
    main()
