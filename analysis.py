#!/usr/bin/python3

#importing from Twitter API/JSON dump
import pandas as pd
import numpy as np
tweets = pd.read_csv("/Users/Guneet/TwitterScrape/tweets.csv")


#adding candidates column to table based on contents in text column in tweets.csv
def get_candidate(row):
    candidates=[]
    text = row["text"].lower()
    if "clinton" in text or "hillary" in text:
        candidates.append("clinton")
    if "trump" in text or "donald" in text:
        candidates.append("trump")
    return",".join(candidates)
               
tweets["candidate"] = tweets.apply(get_candidate,axis=1)

# adding code column specifying state abbreviation from the location of the user

def get_location(row):
    
    code=[]
    states = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'}
    
    text = row["user_location"]
    if text is np.nan:
        text = '-'   
    for key in states:
        if key in text or states[key] in text:
            code.append(states[key])
            break
            
    return ",".join(code)

tweets["code"] = tweets.apply(get_location,axis=1)


# create new column called user_age from data in created and user_created column
from datetime import datetime
tweets["created"] = pd.to_datetime(tweets["created"])
tweets["user_created"] = pd.to_datetime(tweets["user_created"])
tweets["user_age"] = tweets["user_created"].apply(lambda x: (datetime.now() - x).total_seconds() / 3600 / 24 / 365)
cl_tweets = tweets["user_age"][tweets["candidate"]=="clinton"]
tr_tweets = tweets["user_age"][tweets["candidate"]=="trump"]

#Plotting number of tweets mentioning each candidate combination, use your plotly API keys if applicable
import plotly 
plotly.tools.set_credentials_file(username='######', api_key='*******')

import plotly.plotly as py
from plotly.graph_objs import *

import plotly.graph_objs as go

import numpy as np
x0 = cl_tweets
x1 = tr_tweets

trace1 = go.Histogram(
    x=x0,
    histnorm='count',
    name='Clinton',
    

    marker=dict(
        color='blue',
        line=dict(
            color='blue',
            width=0
        )
    ),
    opacity=0.75
)
trace2 = go.Histogram(
    x=x1,
    name='Trump',
    

    marker=dict(
        color='red'
    ),
    opacity=0.75
)
data = [trace1, trace2]
layout = go.Layout(
    title='Tweets mentioning each candidate',
    xaxis=dict(
        title='Twitter account age in years'
    ),
    yaxis=dict(
        title='Number of tweets'
    ),
    barmode='stack',
    bargap=0.2,
    bargroupgap=0.1
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='number-of-tweets',fileopt='extend', auto_open=False)

#Filter out empty cells in code and candidates columns so we can visualize using a choropleth. Also get counts for each
#candidate.

filter1 = tweets["code"]!=""
cleancodes = tweets[filter1]
filter2 = cleancodes["candidate"]!=""
cleantweets = cleancodes[filter2]

cl_states = cleantweets["code"][cleantweets["candidate"]=="clinton"]
tr_states = cleantweets["code"][cleantweets["candidate"]=="trump"]

clcount = cl_states.value_counts()
trcount = tr_states.value_counts()

popularityindex = trcount - clcount
filteredpopularityindex = popularityindex.dropna()

#Visualize tweets by location for Hillary Clinton.

scl = [[0.0, 'rgb(170,170,255)'],[0.2, 'rgb(130,130,255)'],[0.4, 'rgb(120,120,255)'],\
            [0.6, 'rgb(100,100,255)'],[0.8, 'rgb(50,50,255)'],[1.0, 'rgb(0,0,255)']]

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = clcount.index, 
        z = clcount,
        locationmode = 'USA-states',
        text = "Tweets about Cliton",
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Location by the numbers")
        ) ]

layout = dict(
        title = 'Who is talking about Hillary Clinton?',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' )
             ))
    
fig = dict( data=data, layout=layout )
py.plot( fig, filename='hd3-cloropleth-map', fileopt='extend', auto_open=False)

# Visualize tweets by location for Donald Trump. 

scl = [[0.0, 'rgb(255,170,170)'],[0.2, 'rgb(255,130,130)'],[0.4, 'rgb(255,120,120)'],\
            [0.6, 'rgb(255,100,100)'],[0.8, 'rgb(255,50,50)'],[1.0, 'rgb(255,0,0)']]

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = trcount.index, 
        z = trcount,
        locationmode = 'USA-states',
        text = "Tweets about Trump",
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Tweet Locations")
        ) ]

layout = dict(
        title = 'Who is talking about Donald Trump?',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' )
             ))
    
fig = dict( data=data, layout=layout )
py.plot( fig, filename='td3-cloropleth-map',fileopt='extend', auto_open=False )

# Visualize tweet content for Clinton and Trump on state basis

scl = [[0.0, 'rgb(130,130,255)'],[0.2, 'rgb(255,170,170)'],[0.4, 'rgb(255,150,150)'],\
            [0.6, 'rgb(255,100,100)'],[0.8, 'rgb(255,50,50)'],[1.0, 'rgb(255,0,0)']]


data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = filteredpopularityindex.index, 
        z = filteredpopularityindex,
        locationmode = 'USA-states',
        text = "Trump and Clinton together",
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Tweet Majority")
        ) ]

layout = dict(
        title = 'Who are we really talking about?',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' )
             ))
    
fig = dict( data=data, layout=layout )
py.plot( fig, filename='usad3-cloropleth-map', fileopt='extend', auto_open=False)

#Standard Deviation and Mean Calculations

group = tweets.groupby("candidate").agg([np.mean, np.std])
std = group["polarity"]["std"].iloc[1:]
mean = group["polarity"]["mean"].iloc[1:]

data = [go.Bar(
            x=['clinton','trump'],
            y=[mean[0],mean[2]]
    )]
layout = go.Layout(
    title='Mean Tweet Sentiment',
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='meansent', fileopt='extend', auto_open=False)


data = [go.Bar(
            x=['clinton','trump'],
            y=[std[0],std[2]]
    )]
layout = go.Layout(
    title='Standard Deviation of Tweet Sentiment',
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='stdsent', fileopt='extend', auto_open=False)



