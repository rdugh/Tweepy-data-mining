import tweepy
import Twitter_credential


#creating a stream listener
class MyStreamListener(tweepy.StreamListener):
    '''Basic listener class that just print received tweets to stdout.'''
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self,data):
        #print(data)
        try:
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on data:%s' % str(e))
            return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.


class TwitterStreamer():
    '''Class for streaming and processing live tweets'''
    def __init__(self):
        pass
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #This handles Twitter authentication and the connection to the Twitter Streaming API.
        
        #Authentication 
        auth = tweepy.OAuthHandler(Twitter_credential.API_key, Twitter_credential.API_secret_key)# responsibel authenticating our code
        auth.set_access_token(Twitter_credential.Access_token, Twitter_credential.Access_token_secret)
        api = tweepy.API(auth)

        #public_tweets = api.home_timeline()#for tweet in public_tweets:#print(tweet.text)

        #creating a stream
        myStreamListener = MyStreamListener(fetched_tweets_filename)
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

        #Starting a stream
        myStream.filter(track=hash_tag_list)


if __name__=='__main__':
    hash_tag_list=['SDG']
    fetched_tweets_filename='tweets.json'
    twitter_streamer=TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)
