# This script reads a JSON file with tweets and persists all significant data in an sqlite database.

import codecs
import json
import sys
import hashlib
import sqlite3 as lite
from pprint import pprint

status_update_ratio = 1000 # How often should info about number of parsed lines be printed


def main():    
    if len(sys.argv) < 2:
        print "Usage: python tweets_persister.py <file_name>"
        return

    con = lite.connect('test.db')

    with con:        
        cur = con.cursor()    

        # Parse the file
        counter = 0
        with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
            for line in f:    
                try:
                    first_processing(line, cur)
                except:
                    print "!!! exception at %d" % counter

                # Print status
                if (counter % status_update_ratio == 0):
                    con.commit() 
                    print "[1st stage] line %d" % counter
                counter = counter + 1        
        con.commit() 

        # Parse the file again as some records cannot be calculated without 
        # full overview of users and tweets, gathered in the first parsing
        counter = 0
        with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
            for line in f:    
                try:
                    second_processing(line, cur)
                except:
                    print "!!! exception at %d" % counter

                # Print status
                if (counter % status_update_ratio == 0):
                    con.commit() 
                    print "[2nd stage] line %d" % counter
                counter = counter + 1        
        con.commit() 




def first_processing(line, cur):
    data = json.loads(line)
    
    id =                    data['id']
    timestamp =             data['timestamp']
    text =                  data['text']
    language =              data['language']
    hashtags =              data['hashtags']
    user_id =               data['user']['id']
    user_name =             data['user']['name']
    user_followers_count =  data['user']['followers_count']
    user_statuses_count =   data['user']['statuses_count']
    user_language =         data['user']['language']

    lang_id = lang_hash(language)
    user_lang_id = lang_hash(user_language)

    cur.execute("INSERT OR IGNORE INTO language VALUES(?, ?)", (lang_id, language))
    cur.execute("INSERT OR IGNORE INTO user VALUES(?, ?, ?, ?, ?)", (user_id, user_name, user_followers_count, user_statuses_count, user_lang_id))
    cur.execute("UPDATE user SET followers_count=?, statuses_count=? WHERE user.id=?", (user_followers_count, user_statuses_count, user_id))
    cur.execute("INSERT INTO tweet VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (id, user_id, timestamp, text, None, None, None, lang_id))
               
    for hashtag in hashtags:         
        hashtag_id = hashtag_hash(hashtag) 
        cur.execute("INSERT OR IGNORE INTO hashtag VALUES(?, ?)", (hashtag_id, hashtag))  
        cur.execute("INSERT INTO hashtag_in_tweet VALUES(?, ?)", (hashtag_id, id))  




def second_processing(line, cur):
    data = json.loads(line)
    
    id =                    data['id']
    user_id =               data['user']['id']
    reply_to_user =         data['reply_to_user']
    reply_to_tweet =        data['reply_to_tweet']
    retweet_of =            data['retweet_of']
    user_mentions =         data['user_mentions']

    if reply_to_user != None:
        cur.execute("UPDATE tweet SET reply_to_user=? WHERE tweet.id=? AND (SELECT COUNT(id) FROM user WHERE user.id=?) > 0", (reply_to_user, id, reply_to_user))

    if reply_to_tweet != None:
        cur.execute("UPDATE tweet SET reply_to_tweet=? WHERE tweet.id=? AND (SELECT COUNT(id) FROM tweet WHERE tweet.id=?) > 0", (reply_to_tweet, id, reply_to_tweet))

    if retweet_of != None:
        cur.execute("UPDATE tweet SET retweet_of=? WHERE tweet.id=? AND (SELECT COUNT(id) FROM tweet WHERE tweet.id=?) > 0", (retweet_of, id, retweet_of))

    for mention in user_mentions:   
        cur.execute("INSERT INTO mention_in_tweet SELECT ?, ? WHERE (SELECT COUNT(id) FROM user WHERE user.id=?) > 0", (mention, id, user_id))  




def lang_hash(language):
    lang_str = language + "\0"
    val = 0
    for i in range (0, 3):
        val = val * 1000
        val = val + ord(lang_str[i])
    return val


def hashtag_hash(hashtag):
    return abs(hash(hashtag)) % (10000000000)

    # print id
    # print timestamp
    # print text
    # print reply_to_user
    # print reply_to_tweet
    # print language
    # print retweet_count
    # print favorite_count
    # print retweet_of
    # print hashtags
    # print user_mentions
    # print user_id
    # print user_name
    # print user_followers_count
    # print user_statuses_count
    # print user_language



if __name__ == '__main__':
    main()