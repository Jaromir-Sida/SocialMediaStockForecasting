# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:50:02 2020

@author: jaromir
"""
# https://pypi.org/project/GetOldTweets3/
import GetOldTweets3 as got
import pandas as pd
import os
import time

src_file_path = r'c:\Users\jaromir\OneDrive\UoM\100_Disertation\02_SrcData'

def to_dataframe(tweets):
    """Coverts Tweet object to Pandas DataFrame. 
        
    parameters : tweets : GetOldTweets3.Tweet 
    
    output : pandas.DataFrame
    """
    df = pd.DataFrame(columns=['username', 'to', 'text', 'retweets',
                               'favorites', 'replies', 'id', 'permalink',
                               'author_id', 'date', 'formatted_date',
                               'hashtags', 'mentions', 'geo', 'urls'])
    
    for idx, tweet in enumerate(tweets):
        df.loc[idx,'username'] =tweet.username
        df.loc[idx,'to'] =tweet.to
        df.loc[idx,'text'] =tweet.text
        df.loc[idx,'retweets'] =tweet.retweets
        df.loc[idx,'favorites'] =tweet.favorites
        df.loc[idx,'replies'] =tweet.replies
        df.loc[idx,'id'] = tweet.id
        df.loc[idx,'permalink'] =tweet.permalink
        df.loc[idx,'author_id'] =tweet.author_id
        df.loc[idx,'date'] =tweet.date
        df.loc[idx,'formatted_date'] =tweet.formatted_date
        df.loc[idx,'hashtags'] =tweet.hashtags
        df.loc[idx,'mentions'] =tweet.mentions
        df.loc[idx,'geo'] =tweet.geo
        df.loc[idx,'urls'] =tweet.urls

    return df

def to_csv(df, path, file_name):
    """ Saves dataframe as csv."""
    if os.path.exists('path') == True:
        if os.path.isfile(path+ "\\" +file_name+".csv") == True:
            df.to_csv(path+ "\\" +file_name+".csv")
            print("File saved succesfully to:" + path)
            return
        else:
            confirmation = input("Do you want to overwrite current file Y/N ?").lower()
            if confirmation ==str(confirmation) == 'y':
                df.to_csv(path+ "\\" +file_name+".csv")
                print("File saved succesfully to:" + path)
                return
            else:
                print("File NOT saved!")
                return
    else:
        print("File not saved.")
    

start = time.time()
tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#AAPL')\
                                           .setSince("2015-05-01")\
                                           .setUntil("2015-09-30")\
                                           .setEmoji("unicode")\
                                           .setMaxTweets(50)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)
end = time.time()
print(end-start)

# Get tweeets by user name
tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama whitehouse")\
                                           .setMaxTweets(2)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]


# Get twets and preserve emojis
tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama")\
                                           .setSince("2015-09-10")\
                                           .setUntil("2016-01-01")\
                                           .setMaxTweets(1)\
                                           .setEmoji("unicode")
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)


print(tweet.text)



%%time