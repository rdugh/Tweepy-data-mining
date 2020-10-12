import tweepy
import Twitter_credential
import numpy as np
import pandas as pd
import datetime

'''
class TwitterAuthenticator():
    def authenticate_twitter_app(self):'''

def w_file_info(info):
    with open('File Information','a') as E:
        E.write(str(datetime.datetime.now()))
        E.write(str(info))        

#creating a stream listener
class MyStreamListener(tweepy.StreamListener):
    '''Basic listener class that just print received tweets to stdout.'''
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.num_tweets=0

    def on_data(self,data):
        #print(data)
        try:
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            w_file_info(str(e))
            print('Error on data:%s' % str(e))
            return True

    def on_status(self, status):
        record={'Text':status.text,'Created At':status.created_at}
        print(record)
        self.num_tweets+=1
        if self.num_tweets<5:
            #collection.insert(record)
            return True
        else:
            return False

    def on_error(self, status_code):
        print(status_code)
        w_file_info(status_code)
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
    hash_tag_list=['#SDGs','#DayOfTheGirl','#ZeroHunger','#ForNature']
    d=datetime.datetime.now()
    fetched_tweets_filename='Testtweets'+str(d.year)+str(d.month)+str(d.day)+'_'+str(d.hour)+str(d.minute) +'.json'
    twitter_streamer=TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)
    #Use control+C to cut your run
