# This script processes a CSV file and creates a cfinder graph file.

import codecs

# TWEET_ID
# TWEET_TIMESTAMP
# ID_RETWEETUJACEGO
# NAME_RETWEETUJACEGO
# LANG_RETWEETUJACEGO
# ID_RETWEETOWANEGO
# NAME_RETWEETOWANEGO
# LANG_RETWEETOWANEGO

user_ids = []
nodes = []
nodeid = 0
edgeid = 0

fileName = 'retweet_lfc_real'

mention_file = codecs.open(fileName + '.csv', encoding='utf-8')
for line in mention_file.readlines():
    tokens = line.split(";|")
    if (len(tokens) == 8):
        if (not int(tokens[5]) in user_ids):
            user_ids.append(int(tokens[5]))

print "user_ids: ", len(user_ids)


with codecs.open(fileName + '_cfinder.txt', "w", encoding='utf-8') as output_file:
    mention_file = codecs.open(fileName + '.csv', encoding='utf-8')
    for line in mention_file.readlines():
        tokens = line.split(";|")
        if (len(tokens) == 8):
            if (int(tokens[2]) in user_ids):
                if (int(tokens[5]) in user_ids):
                    output_file.write('%s %s 1\n' %
                                      (tokens[3].replace('"', '').replace(' ', '').replace('\t', '_'), tokens[6].replace('"', '_').replace(' ', '_').replace('\t', '_')))


