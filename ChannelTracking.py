#!/usr/bin/env python
# coding: utf-8

# In[31]:


from googleapiclient.discovery import build
import pandas as pd
from datetime import date
import numpy as np
import time
import json


# In[32]:


api_key = 'AIzaSyB7EHy2ZKpfPTY56yRVuu7a8lChfB-IVjw'
youtube = build('youtube', 'v3', developerKey=api_key)



while True:
    
    with open('/princeton_data/source_files/metadata_channels.json') as json_file:
            channelsJ=[]
            for line in json_file:
                channelsJ.append(json.loads(line))

    ids=[]
    titles=[]
    for i in channelsJ:
        try:
            ids.append(i['id'])
            titles.append(i['title'])
        except:
            pass
    channels=pd.DataFrame()
    channels['id']=ids
    channels['name']=titles

    try:
        track=pd.read_csv('/princeton_data/source_files/daily_logging_channels.csv')
    except:
        track=pd.DataFrame(columns=['date','title','id','views','subs','videoCount'])
    try:
        rmChannel=pd.read_csv('/princeton_data/source_files/removedChannels.csv')
    except:
        rmChannel=pd.DataFrame(columns=['date','ChannelId','Channel'])
        
    day=date.today().strftime('%Y-%m-%d')
    for i in channels['id']:
        checked=False
        for j in track[track['date']==day]['id']:
            if j==i:
                checked=True
        if not checked:
            req=youtube.channels().list(part=['id','statistics','snippet'],id=i)
            q=req.execute()
            add=[]
            add.append(day)
            try:
                add.append(q['items'][0]['snippet']['title'])
                add.append(q['items'][0]['id'])
                add.append(q['items'][0]['statistics']['viewCount'])
                try:
                    add.append(q['items'][0]['statistics']['subscriberCount'])
                except:
                    add.append(-1)
                add.append(q['items'][0]['statistics']['videoCount'])
                if i in rmChannel['ChannelId'].to_list():
                    rmChannel.loc[rmChannel['ChannelId']==i,'back_online']=True
                track.loc[len(track)]=add
            except:
                try:
                    if all(rmChannel[rmChannel['ChannelId']==i]['back_online'] == True):
                        add2=[]
                        channel=channels[channels['id']==i]['name'].iloc[0]
                        add.append(i)
                        add.append(channel)
                        add2.append(day)
                        add2.append(channel)
                        add2.append(i)
                        add2.append(np.nan)
                        add2.append(np.nan)
                        add2.append(np.nan)
                        add.append(False)
                        rmChannel.loc[len(rmChannel)]=add
                        track.loc[len(track)]=add2
                except:
                        add2=[]
                        channel=channels[channels['id']==i]['name'].iloc[0]
                        add.append(i)
                        add.append(channel)
                        add2.append(day)
                        add2.append(channel)
                        add2.append(i)
                        add2.append(np.nan)
                        add2.append(np.nan)
                        add2.append(np.nan)
                        add.append(False)
                        rmChannel.loc[len(rmChannel)]=add
                        track.loc[len(track)]=add2
    track.to_csv('/princeton_data/source_files/daily_logging_channels.csv',index=False)
    rmChannel.to_csv('/princeton_data/source_files/removedChannels.csv',index=False)
    print('done ',day)
    time.sleep(86400)
