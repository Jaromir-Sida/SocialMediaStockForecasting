# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:48:23 2020

@author: jaromir
"""

import pandas as pd
from glob import glob
import re
import yfinance as yf
import matplotlib.pyplot as plt

src_data = r'c:\Users\jaromir\OneDrive\UoM\100_Disertation\02_SrcData'

filenames = glob(src_data+'\*.csv')
df = pd.DataFrame()

for file in filenames:
    # read a csv from source folder
    stock = pd.read_csv(file)
    # parese the name of the file to extract the ticker name and save it 
    # as a new attribute
    stock['ticker'] = re.search('#[A-Z]+_',file).group(0)[1:-1]
    # concatenate the csv with the rest of the DataFrame
    df = pd.concat([df, stock], axis=0)

# Get Finance data
start_date = "2019-03-19"
end_date = "2020-06-19"
stock_price = pd.DataFrame()

for ticker in df.ticker.unique():
    tick = yf.download(ticker, start=start_date, end=end_date)
    tick['ticker'] = ticker
    stock_price = pd.concat([stock_price, tick], axis=0)
# get historical market data

# Tokenization

# tokenization into sentences
from nltk.tokenize import sent_tokenize
print(sent_tokenize(df.iloc[0,:].text))

# tokenization into words
from nltk.tokenize import word_tokenize
print(word_tokenize(df.iloc[0,:].text))

# Frequency distribution
from nltk.probability import FreqDist
fdist = FreqDist(word_tokenize(df.iloc[0,:].text))

print(FreqDist(word_tokenize(df.iloc[0,:].text)))
print(fdist.most_common)

# plot word distribution
fdist.plot(30,cumulative=False)
plt.show()

# stop words
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
stop_words=set(stopwords.words("english"))
print(stop_words)

# Removing stop words

filtered_sent=[]
for w in word_tokenize(df.iloc[0,:].text):
    if w not in stop_words:
        filtered_sent.append(w)
print("Tokenized Sentence:",word_tokenize(df.iloc[0,:].text))
print("Filterd Sentence:",filtered_sent)


# Stemming
from nltk.stem import PorterStemmer

ps = PorterStemmer()

stemmed_words=[]
for w in filtered_sent:
    stemmed_words.append(ps.stem(w))

print("Filtered Sentence:",filtered_sent)
print("Stemmed Sentence:",stemmed_words)


# Lemmatizaion

from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()

lemmatized_words=[]
for w in filtered_sent:
    lemmatized_words.append(lem.lemmatize(w,"v"))

print("Filtered Sentence:",filtered_sent)
print("Lemmatized Sentence:",lemmatized_words)

# POS tagging
nltk.download('averaged_perceptron_tagger')
pos = nltk.pos_tag(filtered_sent)

from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

lemmatized_words_pos=[]
for word_tup in nltk.pos_tag(filtered_sent):
    current_pos = get_wordnet_pos(word_tup[1])
    if current_pos == '':
        lemmatized_words_pos.append(lem.lemmatize(word_tup[0]))
    else:
        lemmatized_words_pos.append(lem.lemmatize(word_tup[0],current_pos))
    
print("Lemmatized Sentence:",lemmatized_words)
print("Lemmatized Sentence with POS:",lemmatized_words_pos)