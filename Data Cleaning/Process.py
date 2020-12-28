# import library

def P(T):
    import pandas as pd
    import emoji#checking if a character is an emojis
    from collections import Counter

    #remove the formating of source
    T['source']=T['source'].str.lower()
    T['source']=T['source'].str.findall('>([^<]+?)<').apply(lambda x:x[0] if len(x)>=1 else '')

    #import location dictionary and generate country
    T['location']=[T.loc[k,'place']['country_code'] if not pd.isnull(T.loc[k,'place']) else i['location'] for k,i in enumerate(T['user'])]
    
    Trans=pd.read_csv('/Users/livi/Documents/2020 Fall/data mining/Proposal/Tweepy related files/transloc.csv',index_col=0)
    Trans['googlemap']=Trans['googlemap'].apply(eval)
    Trans.set_index('UserInfo',inplace=True)
    locdict=Trans.T.to_dict('records')
    locdict=locdict[0]
    kys=list(locdict.keys())
    for k in kys:
        if locdict[k]==None:
            del locdict[k]
        elif len(locdict[k])!=0:
            if 'address_components' in locdict[k][0]:
                for ii in locdict[k][0]['address_components']:
                    if 'country' in ii['types']:
                        locdict[k]=ii['long_name']
                    else:
                        if len(locdict[k])>1:
                            if 'address_components' in locdict[k][1]:
                                for ii in locdict[k][1]['address_components']:
                                    if 'country' in ii['types']:
                                        locdict[k]=ii['long_name']
            else:
                del locdict[k]
        else:
            del locdict[k]
        
    ## Generate the column 
    l=[]
    for i in T['location']:
      try:
        l.append(locdict[i])
      except:
        l.append(float('nan'))
    T['CountryCode']=l
    print('Finish Generate Country Code')



    #Generate Extended tweets and SDGs
    for i in range(len(T)):
        quote=None
        comment=None
        #prepare quote part
        if not pd.isnull(T.loc[i,'quoted_status']):
            try:
                quote=T.loc[i,'quoted_status']['extended_tweet']['full_text']
            except:
                quote=T.loc[i,'quoted_status']['text']
                #print('no extended_tweet for quote',i)
        #prepare comment part
        if pd.isnull(T.loc[i,'extended_tweet']):
            if pd.isnull(T.loc[i,'retweeted_status']):
                try:
                    comment=T.loc[i,'text']
                except:
                    print('no text',i)
            else:
                try:
                    comment=T.loc[i,'retweeted_status']['extended_tweet']['full_text']
                except:
                    comment=T.loc[i,'retweeted_status']['text']
                    #print('no extended_tweet for retweeted status',i)
        else:
            try:
                comment=T.loc[i,'extended_tweet']['full_text']
            except:
                print('no extended_tweet',i)
        #combine quote and comments
        if pd.isnull(quote):
            T.loc[i,'extended_tweet']=comment
        else:
            T.loc[i,'extended_tweet']='\"'+comment+' \" '+quote
    ## remove some useless information
    T['extended_tweet']=T['extended_tweet'].str.replace("http\S+","")
    #T['extended_tweet']=T['extended_tweet'].str.replace("@\S+","")
    T['extended_tweet']=T['extended_tweet'].str.replace("&amp","")
    print('Finish Generate Extended Tweets')

    T=T.reset_index(drop=True)
    T['extended_tweet']=T['extended_tweet'].str.lower()
    T['SDG']=T['extended_tweet'].str.upper()
    T['SDG']=T['SDG'].str.findall('(SDG\d+)')
    print('Finish Generate SDGs')

    # Generate User Information and hashtags
    T['id']=[i['id']for i in T['user']]
    T['name']=[i['name']for i in T['user']]
    T['screen_name']=[i['screen_name'] for i in T['user']]
    T['url']=[i['url'] for i in T['user']]
    T['friends_count']=T['user'].apply(lambda x:x['friends_count'])
    T['followers_count']=T['user'].apply(lambda x:x['followers_count'])
    T['hashtags']=T['extended_tweet'].str.findall('#\S+')
    print('Finish Generate UserInfo and Hashtags')

    # Prepare lemmatized analysis and tokenized extended tweets
    def char_is_emoji(character):
        return character in emoji.UNICODE_EMOJI#does the text contain an emoji?
    def text_has_emoji(text):
        for character in text:
            if character in emoji.UNICODE_EMOJI:
                return True
        return False#remove the emoji
    def deEmojify(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')

    T['extended_tweet']=T['extended_tweet'].apply(lambda x:deEmojify(x))

    import spacy
    from spacy.lemmatizer import Lemmatizer
    from spacy.lookups import Lookups
    sp = spacy.load('en')
    lookups = Lookups()
    lemm = Lemmatizer(lookups)

    def lemma_function(text):
        dummy = []
        #this is just a test to see if it works
        for word in sp(text):
            dummy.append(word.lemma_)    
        return ' '.join(dummy)
    T['extended_tweet_lemmatized'] = T['extended_tweet'].apply(lambda x: lemma_function(x))
    T['extended_tweet_lemmatized']=T['extended_tweet_lemmatized'].apply(lambda x:x.replace('-PRON-',''))
    print('Finish deemoji and lemmatization')


    # Generate Sentiment Scores
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()
    def sentiment_analyzer_scores(sentence):
        score = analyser.polarity_scores(sentence)
        print("{:-<40} {}".format(sentence, str(score)))
    T['neg'] = T['extended_tweet_lemmatized'].apply(lambda x:analyser.polarity_scores(x)['neg'])
    T['neu'] = T['extended_tweet_lemmatized'].apply(lambda x:analyser.polarity_scores(x)['neu'])
    T['pos'] = T['extended_tweet_lemmatized'].apply(lambda x:analyser.polarity_scores(x)['pos'])
    T['compound'] = T['extended_tweet_lemmatized'].apply(lambda x:analyser.polarity_scores(x)['compound'])
    print('Finish Generate Sentiment Score')
    return T