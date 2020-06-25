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
    if os.path.exists(path) == True:
        if os.path.isfile(path+ "\\" +file_name+".csv") == False:
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
        
def retrieve_tweets(search_query, start_date, end_date, path, max_limit, language,
                    near):
    """ Dowload tweets and saves them to a csv file"""
    
    # search criteria
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_query)\
                                               .setSince(start_date)\
                                               .setUntil(end_date)\
                                               .setEmoji("unicode")\
                                               .setMaxTweets(max_limit)\
                                               .setLang(language)\
                                               .setNear(near)
    # get tweets
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    
    # store downloaded tweets into a dataframe
    df = to_dataframe(tweet)
    print(df.shape)
    length = df.shape[0]
    # save dataframe into a csv file
    to_csv(df, path, search_query+"_"+start_date+"_"+end_date)
    
    del df
    return length

time_stats = pd.DataFrame(columns=['query','start_date','end_date','count','time'])

trg_file_path = r'c:\Users\jaromir\OneDrive\UoM\100_Disertation\02_SrcData'
start_date = "2019-03-19"
end_date = "2020-06-19"
language = 'en'
near = '840'
tickers = ['#KO', '#XOM','#TSLA','#JPM','#DIS']
max_limit = 10000

for idx, ticker in enumerate(tickers):
    start = time.time()
    tweet_count = retrieve_tweets(ticker, start_date, end_date, trg_file_path, max_limit,
                                  language, near)
    end = time.time()
    total_time = end-start

    stats = pd.DataFrame({'query':ticker,'start_date':start_date,'end_date':end_date,
                      'count': tweet_count, "time":total_time}, index=[idx])

#    time_stats = pd.concat([time_stats,stats], axis = 0 )
    pd.concat([time_stats, stats], axis=0)

#if __name__ == "__main__":
#
#end = time.time()
#print(end-start)
    
# XOM - energy
# TSLA - automotive
# JPM - banking 
# DIS - media
# KO - food
    
