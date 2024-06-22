#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df=pd.read_csv('GE_2024_Results.csv')
df


# In[3]:


df.info()


# In[4]:


df.isnull().sum()


# In[5]:


df['EVM Votes'] = df['EVM Votes'].str.replace('-', '0')
df['Postal Votes'] = df['Postal Votes'].str.replace('-', '0')
df['% of Votes'] = df['% of Votes'].str.replace('-', '0')

new_datatype={'EVM Votes':'int64','Postal Votes':'int64','% of Votes':'float64'}
df=df.astype(new_datatype)


# In[6]:


df


# In[7]:


df.info()


# In[8]:


#What is the total number of candidates across all constituencies?
df['Candidate'].count()


# In[9]:


#How many constituencies are there in total?
df['Constituency'].drop_duplicates().count()


# In[10]:


# What is the average voter turnout (total votes) per constituency across the entire dataset?
df.groupby('Constituency')['Total Votes'].mean().sort_values(ascending=False).to_frame()


# In[11]:


#which party recieved the highest number of total votes?
df.groupby('Party')['Total Votes'].max().sort_values(ascending=False).to_frame().reset_index().head(1)


# In[12]:


#which party won the most number of seats?
win=df[df['Result']=='Won']
win.groupby('Party').count()['ID'].sort_values(ascending=False).head(1)


# In[13]:


#what is distribution of seats won by each party?
dist_party=win.groupby('Party').count().reset_index().sort_values(by='ID',ascending=False)[["Party","Result"]].rename(columns={'Result':'Seats'})
dist_party.set_index('Party')


# In[14]:


dist_party.plot(kind='bar',x='Party',y='Seats',figsize=(15,7))
plt.ylabel('No. of seats won by party')
plt.xlabel('Name of party')
plt.title('No. of seats VS party')
plt.show()


# In[15]:


# the top 10 candidates based on the total votes received
win.groupby('Candidate')['Total Votes'].max().sort_values(ascending=False).reset_index().head(10)


# In[16]:


# candidate won their seats by the largest margins
win= df[df['Result'] == 'Won'].copy()
win['% of Votes'] = pd.to_numeric(win['% of Votes'], errors='coerce')
win.loc[:, 'Margin'] = win['Total Votes'] * (win['% of Votes'] / 100)
largest_margin_candidate = win.loc[win['Margin'].idxmax()]
largest_margin_candidate[['Candidate', 'Party', 'Margin']]


# In[17]:


win


# In[18]:


#the top 10 closest races(smallest margins)?
smallest_margins=win['Margin'].sort_values(ascending=True).reset_index().head(10)
# win[win['index'].isin(smallest_margins['index'])]
smallest_margins['Margin']


# In[19]:


#total number of votes in every states
df.groupby('State')['Total Votes'].sum().sort_values(ascending=False).reset_index()


# In[20]:


# state had the highest voter turnout
df.groupby('State')['Total Votes'].sum().sort_values(ascending=False).reset_index().head(1).rename(columns={'Total Votes':'Highest Voter Turnout'})


# In[21]:


#different parties perform in every state
df.groupby(['State','Party']).agg({'Candidate':'count','Total Votes':'sum'}).rename(columns={'Candidate': 'Seats Won'}).reset_index()


# In[22]:


#number of seats won by top 5 parties
dist_party=win.groupby('Party').count().reset_index().sort_values(by='ID',ascending=False)[["Party","Result"]].rename(columns={'Result':'Seats'}).head(5)
dist_party.set_index('Party').reset_index()
dist_party.plot(kind='bar',x='Party',y='Seats',color=('red','green','orange','yellow','brown'))
plt.xlabel('top 5 Parties')
plt.ylabel('Number of seats')
plt.title('Top five party analysis on the basis of no. of seats')


# In[23]:


#total number of votes in across each states
votes_state=df.groupby('State')['Total Votes'].sum().sort_values(ascending=False).reset_index()
votes_state.plot(kind='bar',y='Total Votes',x='State',figsize=(15,7))
plt.xlabel('states')
plt.ylabel('total votes')
plt.title('total votes across each state')
plt.show()


# In[24]:


#a pie chart representing the percentage of total votes received by each major party
major_parties=df.groupby('Party')['Total Votes'].sum().reset_index().sort_values(by='Total Votes',ascending=False).head(5)
plt.figure(figsize=(10, 7))
plt.pie(major_parties['Total Votes'], labels=major_parties['Party'], autopct='%1.1f%%', startangle=140)
plt.title('Percentage of Total Votes Received by Each Major Party')
plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
plt.show()


# In[25]:


win


# In[26]:


#relation between EVM Votes and Postal Votes for the winning candidate
win_cd=win[['EVM Votes','Postal Votes']]
win_cd


# In[27]:


sns.scatterplot(data=win,x='EVM Votes',y='Postal Votes')


# In[ ]:





# In[ ]:




