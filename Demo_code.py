import tweepy
import Twitter_credential
import datetime
import time
from time import gmtime, strftime

'''
class TwitterAuthenticator():
    def authenticate_twitter_app(self):'''

def w_file_info(info,filename='current'):
    d=datetime.datetime.now()
    fileinfo='FileInformation'+str(d.year)+str(d.month)+str(d.day)+'_'+str(d.hour) +'.txt'
    with open(fileinfo,'a') as E:
        print('Something happended to file ',filename,'I am writing a file...\n')
        E.write(str(datetime.datetime.now())+'\n')
        E.write(str(filename)+':')
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
            w_file_info(str(e),self.fetched_tweets_filename)
            print('Error on data:%s' % str(e))
            return True
        return True

    '''def on_status(self, status):
        print(status)
        return
        record={'Text':status.text,'Created At':status.created_at}
        print(record)
        self.num_tweets+=1
        if self.num_tweets<5:
            #collection.insert(record)
            return True
        else:
            return False'''

    def on_error(self, status_code):
        print(status_code)
        w_file_info(status_code)
        if status_code == 420:
            #returning False in on_error disconnects the stream
            time.sleep(10)

        if status_code==429:
            print('Waiting on limit')
            w_file_info('Waiting on limit 16min')
            time.sleep(15*60+1)
        else:
            print('Unexpected. Will retry in 10 s.')
            w_file_info('Unexpected. Will retry in 10 s.')
            time.sleep(10)

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
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended')

        #Starting a stream
        myStream.filter(languages=["en"],track=hash_tag_list,is_async=True)
        #stream.filter(languages=["en"], track=search_words, is_async=True) 


if __name__=='__main__':
    hash_tag_list=['#SDGs','#SDG','#SDGoals','#Act4SDGs','#2030Agenda','sdg1', 'sdg2', 'sdg3', 'sdg4', 'sdg5', 'sdg6', 'sdg7', 'sdg8', 'sdg9', 'sdg10', 'sdg11', 'sdg12', 'sdg13', 'sdg14', 'sdg15', 'sdg16', 'sdg17','SDG1', 'SDG2', 'SDG3', 'SDG4', 'SDG5', 'SDG6', 'SDG7', 'SDG8', 'SDG9', 'SDG10', 'SDG11', 'SDG12', 'SDG13', 'SDG14', 'SDG15', 'SDG16', 'SDG17','#poverty','#zerohunger','#globalhealth','#education','#genderequaslity','#water','#energy','#decentwork','#economicgrowth','#ideas','#socialjustice','#sustainablecities','#sparetosave','#climateaction','#ocean','#lifeonland','#justice','#peace','#NOagenda2030','#NoAgenda21','#NoSDGs','#NoAgenda2021','#BanSDGs','#BANAgenda2030','#fuckagenda2030','#SayNoToAgenda2030','#SayNoToAgenda21','StopAgenda2030','stopsdgs','NoUNAgenda2030','NoUNAgenda21','NoUNAGENDA30','NoUNAgenda','StopGlobalGoals','noGlobalGoals','GlobalGoals propaganda','GlobalGoals Hypocrisy','SDGs propaganda','agenda2030 propaganda','Agenda2030 Scam','sdgs hoax','globalgoals hoax','sdgs scam','fightagenda2030','AGAINSTAGENDA2030','AGAINSTAGENDA21','FightAgenda21']    
    d=datetime.datetime.now()
    fetched_tweets_filename='Testtweets'+str(d.year)+str(d.month)+str(d.day)+'_'+str(d.hour)+str(d.minute) +'.json'
    twitter_streamer=TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)
    print('Start Running, Use ctrl+C to stop')
    #Use control+C to cut your run
