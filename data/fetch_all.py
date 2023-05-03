import requests
import requests.auth
import pandas as pd
import re
import nltk
import praw
import asyncio
import datetime as dt
from psaw import PushshiftAPI


### using a predefined and cleaned dataset 


politics = ['Libertarian' 'Anarchism' 'socialism' 'progressive' 'Conservative'
 'americanpirateparty' 'democrats' 'Liberal' 'Republican'
 'LibertarianLeft' 'Liberty' 'Anarcho_Capitalism' 'alltheleft' 'neoprogs'
 'labor' 'blackflag' 'GreenParty' 'democracy' 'IWW' 'Marxism'
 'Objectivism' 'LibertarianSocialism' 'Capitalism' 'feminisms'
 'republicans' 'Egalitarianism' 'anarchafeminism' 'SocialDemocracy'
 'Postleftanarchism' 'AnarchoPacifism' 'conservatives' 'voluntarism'
 'PirateParty' 'Anarchist' 'Communist']


df_all = pd.read_csv("archive/the-reddit-climate-change-dataset-posts.csv")
df_all = df_all.dropna(subset=['selftext'])
print(df_all.shape)



# get all of the values of subreddit.name
subreddits_list = list(df_all["subreddit.name"].unique())
for subred in subreddits_list:
    if subred in politics:
        print(subred)
print(subreddits_list)