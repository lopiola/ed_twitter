# This script opens a tweet stream from twitter, filters tweets that contain
# tags listed in "tags.txt" and saves them to the disk - "tweets-json.txt"

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey = 'ckey'
csecret = 'csecret'
atoken = 'atoken'
asecret = 'asecret'

tags = []

def load_tags():
	with open("tags.txt") as tagsfile:
		tags = tagsfile.readlines()
	tags = [tag.strip('\n') for tag in tags]
	return tags
 
class listener(StreamListener):
	
	def on_data(self, data):
		with open("tweets-json.txt", "a") as myfile:
			myfile.write(data)
		return True

	def on_error(self, status):
		print status

tags = load_tags()
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=tags)
