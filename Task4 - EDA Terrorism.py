#!/usr/bin/env python
# coding: utf-8

# # GRIP @ THE SPARKS FOUNDATION
# ### Data Science and Business Analytics 

# ## Exploratory Data Analysis on Global Terrorism

# ##### Presented by- Vandana Prajapati

# In[1]:


pip install plotly


# In[7]:


# Import the Libraries.
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import seaborn as sns
from scipy import signal


# In[10]:


data=pd.read_csv("C:\\Users\\Vandana Prajapati\\Downloads\\globalterrorismdb_0718dist.csv",encoding='ISO-8859-1')
data.head()


# #### Check the names of all the columns and select out all the important columns which are needed in analysis.

# In[11]:


pd.set_option("display.max_columns",None)
data.info()


# In[12]:


data.head()


# In[12]:


data['casualities'] = data['nkill'] + data['nwound']
data.shape


# In[13]:


print('Country with Highest Terrorist Attacks:',data['country_txt'].value_counts().index[0])
print('Maximum people killed in an attack:',data['nkill'].max())
print("Year with the most attacks:",data['iyear'].value_counts().idxmax())
print("Year with the least attacks:",data['iyear'].value_counts().idxmin())
print("Most Attack Types:",data['attacktype1_txt'].value_counts().idxmax())
print("Most Active Group:",data['gname'].value_counts().index[1])


# In[43]:


#rename the columns
data.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','provstate':'state',
                       'region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed',
                       'nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type',
                       'weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
data['Casualities'] = data.Killed + data.Wounded
# filtering out the important data in whole dataset those I'm using further processing.
data=data[['Year','Month','Day','Country','state','Region','city','latitude','longitude','AttackType','Killed',
               'Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive','Casualities']]


# In[37]:


data.head()


# In[19]:


data.isnull().sum() 


# ## Data Visualizations 

# In[1]:


plt.subplots(figsize=(15,6))
sns.countplot('Year',data=data,palette='RdYlGn_r',edgecolor=sns.color_palette('dark',10))
plt.xticks(rotation=90)
plt.title('Number Of Terrorist Activities Each Year')
plt.show()


# In[21]:


plt.subplots(figsize=(15,6))
year_cas = data.groupby('Year').Casualities.sum().to_frame().reset_index()
year_cas.columns = ['Year','Casualities']
sns.barplot(x=year_cas.Year, y=year_cas.Casualities, palette='RdYlGn_r',edgecolor=sns.color_palette('dark',10))
plt.xticks(rotation=90)
plt.title('Number Of Casualities Each Year')
plt.show()  


# In[22]:


plt.subplots(figsize=(15,6))
country_attacks = data.Country.value_counts()[:15].reset_index()
country_attacks.columns = ['Country', 'Total Attacks']
sns.barplot(x=country_attacks.Country, y=country_attacks['Total Attacks'], palette= 'OrRd_r',edgecolor=sns.color_palette('dark',10))
plt.xticks(rotation=30)
plt.title('Number Of Total Attacks in Each Country')
plt.show()


# In[ ]:





# In[23]:


pd.crosstab(data.Year, data.Region).plot(kind='area',figsize=(15,6))
plt.title('Terrorist Activities by Region in each Year')
plt.ylabel('Number of Attacks')
plt.show()


# In[39]:


plt.figure(figsize = (13,7))
sns.countplot(data['AttackType'], 
              order = data['AttackType'].value_counts().index,
              palette = sns.color_palette("flare"))
plt.xlabel('Weapons Used')
plt.ylabel('Resulting Death Count')
plt.title('Forms of Attack')
plt.xticks(rotation = 90)
plt.show()


# In[24]:


plt.subplots(figsize=(15,6))
sns.barplot(data['Country'].value_counts()[:15].index,data['Country'].value_counts()[:15].values,palette='mako')
plt.title('Top Countries Affected')
plt.xlabel('Countries')
plt.ylabel('Count')
plt.xticks(rotation= 90)
plt.show()


# In[25]:


plt.subplots(figsize=(15,6))
count_cas = data.groupby('Country').Casualities.sum().to_frame().reset_index().sort_values('Casualities', ascending=False)[:15]
sns.barplot(x=count_cas.Country, y=count_cas.Casualities, palette= 'OrRd_r',edgecolor=sns.color_palette('dark',10))
plt.xticks(rotation=30)
plt.title('Number Of Total Casualities in Each Country')
plt.show()


# In[26]:


region_attacks = data.Region.value_counts().to_frame().reset_index()
region_attacks.columns = ['Region', 'Total Attacks']
plt.subplots(figsize=(15,6))
sns.barplot(x=region_attacks.Region, y=region_attacks['Total Attacks'], palette='OrRd_r', edgecolor=sns.color_palette('magma',10))
plt.xticks(rotation=90)
plt.title('Number Of Total Attacks in Each Region')
plt.show()


# In[27]:


attack_type = data.AttackType.value_counts().to_frame().reset_index()
attack_type.columns = ['Attack Type', 'Total Attacks']
plt.subplots(figsize=(15,6))
sns.barplot(x=attack_type['Attack Type'], y=attack_type['Total Attacks'], palette='viridis',
            edgecolor=sns.color_palette('dark', 10))
plt.xticks(rotation=90)
plt.title('Number Of Total Attacks by Attack Type')
plt.show()


# In[41]:


cities = data.Target.dropna(False)
plt.subplots(figsize=(20,10))
wordcloud = WordCloud(background_color = 'white',
                     width = 512,
                     height = 384,).generate(' '.join(cities))
plt.axis('off')
plt.imshow(wordcloud)
plt.title('Popular Targets', 
        fontdict={'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        'size': 26,})
plt.show()


# In[28]:


city_attacks = data.city.value_counts().to_frame().reset_index()
city_attacks.columns = ['city', 'Total Attacks']
city_cas = data.groupby('city').Casualities.sum().to_frame().reset_index()
city_cas.columns = ['city', 'Casualities']
# city_cas.drop('Unknown', axis=0, inplace=True)
city_tot = pd.merge(city_attacks, city_cas, how='left', on='city').sort_values('Total Attacks', ascending=False)[1:21]
sns.set_palette('cubehelix')
city_tot.plot.bar(x='city', width=0.8)
plt.xticks(rotation=90)
plt.title('Number Of Total Attacks and Casualities by city')
fig = plt.gcf()
fig.set_size_inches(16,9)
plt.show()


# In[29]:


group_attacks = data.Group.value_counts().to_frame().drop('Unknown').reset_index()[:16]
group_attacks.columns = ['Terrorist Group', 'Total Attacks']
group_attacks


# In[30]:


group_attacks = data.Group.value_counts().to_frame().drop('Unknown').reset_index()[:16]
group_attacks.columns = ['Terrorist Group', 'Total Attacks']
plt.subplots(figsize=(10,8))
sns.barplot(y=group_attacks['Terrorist Group'], x=group_attacks['Total Attacks'], palette='Spectral',
            edgecolor=sns.color_palette('dark', 10))
# plt.xticks()
plt.title('Number Of Total Attacks by Terrorist Group')
plt.show()


# In[31]:


groups_10 = data[data.Group.isin(data.Group.value_counts()[1:11].index)]
pd.crosstab(groups_10.Year, groups_10.Group).plot(color=sns.color_palette('Paired', 10))
fig=plt.gcf()
fig.set_size_inches(18,6)
plt.xticks(range(1970, 2017, 5))
plt.ylabel('Total Attacks')
plt.title('Top Terrorist Groups Activities from 1970 to 2017')
plt.legend(labels=['Al-Shabaab',
                   'Boko Haraam',
                   'FMLN',
                   'IRA',
                   'ISIL',
                   'PKK',
                   'NPA',
                   'FARC',
                   'SL',
                   'Taliban'], loc='upper left')
plt.show()


# In[32]:


# Total Number of people killed in terror attack
killData = data.loc[:,'Killed']
print('Number of people killed by terror attack:', int(sum(killData.dropna())))# drop the NaN values


# In[33]:


# attackData
attackData = data.loc[:,'AttackType']
typeKillData = pd.concat([attackData, killData], axis=1)
typeKillFormatData = typeKillData.pivot_table(columns='AttackType', values='Killed', aggfunc='sum')
typeKillFormatData


# In[34]:


countryData = data.loc[:,'Country']
# countyData
countryKillData = pd.concat([countryData, killData], axis=1)
countryKillFormatData = countryKillData.pivot_table(columns='Country', values='Killed', aggfunc='sum')
countryKillFormatData


# In[45]:


cities = data.Motive.dropna(False)
plt.subplots(figsize=(20,10))
wordcloud = WordCloud(background_color = 'white',
                     width = 512,
                     height = 384,).generate(' '.join(cities))
plt.axis('off')
plt.imshow(wordcloud)
plt.title('Motive for Attacks in Different Cities', 
        fontdict={'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        'size': 26,})
plt.show()


# In[35]:


fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size


# In[36]:


labels = countryKillFormatData.columns.tolist()
labels = labels[:50] #50 bar provides nice view
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[:50]
values = [int(i[0]) for i in values] # convert float to int
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange'] # color list for bar chart bar color 
fig, ax = plt.subplots(1, 1)
ax.yaxis.grid(True)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size
plt.bar(index, values, color = colors, width = 0.9)
plt.ylabel('Killed People', fontsize=20)
plt.xlabel('Countries', fontsize = 20)
plt.xticks(index, labels, fontsize=18, rotation=90)
plt.title('Number of people killed by countries', fontsize = 20)
# print(fig_size)
plt.show()


# ### Conclusion
# - The Hot zone countries of terrorism are Iraq, Afghanistan, Pakistan and India.
# - The Hot zone Regions are Middle East, South Africa, North Africa and North America.
# - The Most commonly used Weapons are Explosive and Firearms.
# - By improving our Defence on Explosive and Firearms will help us to reduce terrorism.
# 
# 

# ## THANK YOU !!!
