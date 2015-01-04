# This script filters out important data from tweets in json format. Discards about 85% of unused
# attributes. 

import codecs
import json
import sys
from pprint import pprint

status_update_ratio = 10000 # How often should info about number of parsed lines be printed


def main():    
    if len(sys.argv) < 2:
        print "Usage: python tweets_compactor.py <file_name>"
        return

    lines = []
    counter = 0
    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        for line in f:            
            with open("processed_tweets.json", "a") as myfile:
                myfile.write(process_line(line) + "\n")

            # Print status
            if (counter % status_update_ratio == 0):
                print "line %d" % counter
            counter = counter + 1



def process_line(line):
    data = json.loads(line)

    retweet_of = None
    if data.get('retweeted_status') != None:
        retweet_of = data['retweeted_status']['id']

    tweet = \
    {
        'id' :              data['id'],
        'timestamp' :       data['timestamp_ms'],
        'text' :            data['text'],
        'reply_to_user' :   data['in_reply_to_user_id'],
        'reply_to_tweet' :  data['in_reply_to_status_id'],
        'language' :        data['lang'],
        'retweet_count' :   data['retweet_count'],
        'favorite_count' :  data['favorite_count'],
        'retweet_of' :      retweet_of,
        'hashtags' :        [ hashtag['text'] for hashtag in data['entities']['hashtags'] ],
        'user_mentions' :   [ mention['id'] for mention in data['entities']['user_mentions'] ],
        'user' :            {
                                'id' :              data['user']['id'],
                                'name' :            data['user']['name'],
                                'followers_count' : data['user']['followers_count'],
                                'statuses_count' :  data['user']['statuses_count'],
                                'language' :        data['user']['lang']
                            }
    }

    return json.dumps(tweet, separators=(',',':'))



if __name__ == '__main__':
    main()