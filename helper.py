import streamlit as st
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd


def fetch_stats(user, df):

    if user != 'All':
        df = df[df['user'] == user]
    
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)

    # no of media messages
    media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # no of links shared
    extractor = URLExtract()
    urls = []
    for message in df['message']:
        urls.extend(extractor.find_urls(message))

    links = len(urls)
        
    return num_messages, num_words, media_messages, links

def most_active_users(df):
    most_active = df['user'].value_counts().head(5)
    
    # contribution to total messages
    total_messages = df.shape[0]
    user_message_count = df['user'].value_counts()
    user_message_count /= total_messages
    user_message_count *= 100
    user_message_count = round(user_message_count, 2).reset_index().rename(columns={'index': 'user', 'user': 'percent'})

    return most_active, user_message_count

def generate_wordcloud(user, df):
    if user != 'All':
        df = df[df['user'] == user]
    
    words = ' '.join(df['message'])
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = None, 
                min_font_size = 10).generate(words)
    df_wc = wordcloud.generate(df['message'].str.cat(sep=" "))
    
    return df_wc

from collections import Counter


def find_most_used_words(user, df):
    if user != 'All':
        df = df[df['user'] == user]

    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted']
    temp = temp[temp['message'] != 'Missed voice call']
    temp = temp[temp['message'] != 'Missed video call']
    temp = temp[temp['user'] != 'group_notification']

    f  = open('C:/Users/anish/Desktop/ML Practice/Whatsapp Chat/App/stop_hinglish.txt', 'r', encoding='utf-8')
    stopwords = f.read()
    f.close()

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word.lower())
    
    ans = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'frequency'])
    return ans






