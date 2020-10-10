import tweepy
import Twitter_credential


#creating a stream listener
class MyStreamListener(tweepy.StreamListener):

    def on_data(self,data):
        print(data)
        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.

#Authentication 
auth = tweepy.OAuthHandler(Twitter_credential.API_key, Twitter_credential.API_secret_key) #responsibel authenticating our code
auth.set_access_token(Twitter_credential.Access_token, Twitter_credential.Access_token_secret)

api = tweepy.API(auth)

'''public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
'''
#creating a stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

#Starting a stream
myStream.filter(track=['SDG'])