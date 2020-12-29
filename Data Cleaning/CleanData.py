#### MISSING STOP WORDS NLTK


# import library
import pandas as pd
import json
from os import listdir
from os.path import join

import Process



#import data, in loop
try:
    del T
except:
    pass
folder=f'/Users/livi/Documents/2020 Fall/data mining/Proposal/Tweepy related files/Tweets/'
columns_wanted=['created_at','source','text','truncated','user','geo', 'place','retweeted_status','quoted_status','is_quote_status','entities','extended_tweet','display_text_range','lang']
FinFolder=listdir(folder)
for file in FinFolder[:]:
    if file.endswith('.json'):
        #with open(join(folder,file),'r') as f:
        T=pd.read_json(join(folder,file),lines=True)
        T=T[T['lang']=='en']
        T.drop(columns=T.columns.difference(columns_wanted),inplace=True)
        T=T[~pd.isnull(T['text'])]
        T=T.reset_index(drop=True)
        print('Finish Import, Start to process')
        T=Process.P(T)

        T.drop(columns=['text','truncated','user','geo','place','retweeted_status','is_quote_status','entities','lang','display_text_range','quoted_status','location'],inplace=True)
        T.to_csv(file.split('.')[0]+'_Cleaned.csv')
        print('*'*100)

