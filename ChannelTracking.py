#!/usr/bin/env python
# coding: utf-8

# In[1]:

from googleapiclient.discovery import build
import pandas as pd
from datetime import date
import numpy as np
import time


# In[2]:


api_key = 'AIzaSyB7EHy2ZKpfPTY56yRVuu7a8lChfB-IVjw'
youtube = build('youtube', 'v3', developerKey=api_key)


# In[3]:


#obtendo dados dos canais
try:
    channels=pd.read_csv('channels.csv')
except:
    channels=pd.DataFrame(columns=['id','name'])
    c1=pd.read_csv("FilteredChannels.csv")
    c2=pd.read_csv("Fb_groups_covid_IOs - youtube_channels.csv")
    #Obtendo os ids dos canais
    ids=[]
    for index, i in c1.iterrows():
        try:
            aux=[]
            ids.append(i['Channel url'].split('channel/')[1])
            aux.append(i['Channel url'].split('channel/')[1])
            aux.append(i['Channel name'])
            channels.loc[len(channels)]=aux
        except:
            pass
    for index, i in c2.iterrows():
        try:
            aux=[]
            ids.append(i['URL to channel'].split('channel/')[1].split('/')[0])
            aux.append(i['URL to channel'].split('channel/')[1].split('/')[0])
            aux.append(i['Youtube Channel Name'])
            channels.loc[len(channels)]=aux
        except:
            pass
    users=[]
    for i in c2['URL to channel']:
        try:
            users.append(i.split('c/')[1].split('/')[0])
        except:
            pass
        try:
            users.append(i.split('user/')[1].split('/')[0])
        except:
            pass
    #conseguindo o id dos usuarios
    for i in users:
        request=youtube.channels().list(part=['id','snippet'],forUsername=i)
        query=request.execute()
        try:
            aux=[]
            ids.append(query['items'][0]['id'])
            aux.append(query['items'][0]['id'])
            aux.append(query['items'][0]['snippet']['title'])
            channels.loc[len(channels)]=aux
        except:
            print('Failed to find username:',i)
    channels.to_csv('channels.csv',index=False)


# In[4]:


try:
    track=pd.read_csv('channelsTracking.csv')
except:
    track=pd.DataFrame(columns=['date','title','id','views','subs','videoCount'])
try:
    rmChannel=pd.read_csv('removedChannels.csv')
except:
    rmChannel=pd.DataFrame(columns=['date','ChannelId','Channel'])


# In[7]:


channels.groupby('id').count()


# In[6]:

while True:
    day=date.today()
    for i in channels['id']:
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
            track.loc[len(track)]=add
        except:
            channel=channels[channels['id']==i]['name'].iloc[0]
            add.append(i)
            add.append(channel)
            rmChannel.loc[len(rmChannel)]=add
            channels=channels[channels['id']!=i]
    track.to_csv('channelsTracking.csv',index=False)
    rmChannel.to_csv('removedChannels.csv',index=False)
    channels.to_csv('channels.csv',index=False)
    time.sleep(86400)



# In[ ]:




