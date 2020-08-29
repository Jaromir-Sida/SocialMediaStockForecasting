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
import glob
import shutil
from datetime import timedelta, date

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
        
def daterange(start_date, end_date):
    
    """ produce a list of dates within an interval"""
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
          
def check_file_existence(path, file_prefix):
    """ verifies an exstince of csv files in given directory"""
    files = glob.glob(path+'\\' + file_prefix + '*.csv')
    
    if len(files) > 0 :
        return True
    else:
        return False

def archive_files(path, file_prefix):
    """ archives all files with certain prefix to a new archvie folder """
    if check_file_existence(path, file_prefix):
        
        cur_time = time.localtime()
        
        year = str(cur_time.tm_year)
        month = str(cur_time.tm_mon).zfill(2)
        day = str(cur_time.tm_mday).zfill(2)
        hour = str(cur_time.tm_hour).zfill(2)
        minute = str(cur_time.tm_min).zfill(2)
        #sec = str(time.localtime().tm_sec).zfill(2)
        
        archive_dir_name = path+"\\00_Archive\\" + year+month+day+"_"+hour+minute
        
        os.mkdir(archive_dir_name)

        files = glob.glob(path+'\\' + file_prefix + '*.csv')
        
        for file in files:
            file_name = os.path.basename(file)
            shutil.move(file, archive_dir_name+"\\"+file_name)

        
def retrieve_tweets(search_query, file_prefix, start_date, end_date, path, max_limit, language,
                    near):
    """ Dowload tweets and saves them to a csv file"""
    
    # archive existing files
    archive_files(path,"$")
    
    batch = 0
    

    for single_date in daterange(start_date, end_date):
        
        if batch == 0 or batch % 15 != 0:
        
            single_date_next = single_date + timedelta(1)
            print(single_date, single_date_next)
            
            start = time.time()
            # search criteria
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_query)\
                                                       .setSince(single_date.strftime("%Y-%m-%d"))\
                                                       .setUntil(single_date_next.strftime("%Y-%m-%d"))\
                                                       .setEmoji("unicode")\
                                                       .setMaxTweets(max_limit)\
                                                       .setLang(language)\
                                                       .setNear(near)
            # get tweets
            tweet = got.manager.TweetManager.getTweets(tweetCriteria)
        
            # store downloaded tweets into a dataframe
            df = to_dataframe(tweet)
            length = df.shape[0]
            # save dataframe into a csv file
            
            full_file_path = path + "\\" + search_query+"_"+start_date.strftime("%Y-%m-%d")+"_"+end_date.strftime("%Y-%m-%d")+".csv"
            
            
            if batch == 0 :
                df.to_csv(full_file_path)
                batch += 1
            else:
                df.to_csv( full_file_path, mode='a', header=False)
                batch += 1
                
            end = time.time()
            total_time = end-start
            print(f"{search_query} --- batch no: {batch} ---length : {length}", total_time)
    
            del df
        else:
            # every 14 batches sleep for 15 minutes to avoid hitting the max limit
            print("going to sleep at:", time.asctime( time.localtime(time.time())))
            time.sleep(15*60)
            batch += 1
            
    return length


trg_file_path = r'c:\Users\jaromir\OneDrive\UoM\100_Disertation\02_SrcData'
start_date = date(2020,3,30)
end_date = date(2020,6,30)
#2020-03-01
#2020-06-30
language = 'en'
near = '840'
tickers = ['$DAL']
max_limit = 1000

for idx, ticker in enumerate(tickers):
    start = time.time()
    tweet_count = retrieve_tweets(ticker, "$", start_date, end_date, trg_file_path, max_limit,
                                  language, near)
    end = time.time()
    total_time = end-start
