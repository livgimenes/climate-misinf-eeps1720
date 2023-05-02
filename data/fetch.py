import requests
import requests.auth
import pandas as pd
import re
import nltk
import praw
import asyncio
import datetime



# You might have to do pip install emoji
import emoji



#### Requesting a token ####
# NOTE: This requests a token, which should work for more than one call, for security reasons the password is not on display, but if you need to request ask Livia

username = "project-user"
password = ""
app_client_id = "dyczxLp57fVfQrBb4epVQA"
app_secret = "CEpQfSvjR0aJ2-0deD7xyEvIv4uF5A"

client_auth = requests.auth.HTTPBasicAuth(app_client_id, app_secret)
post_data = {"grant_type": "password", "username": username, "password": password}
headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}

# response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
# TOKEN = response.json()['access_token']

#### Response received ####


###### Getting the main corpus of data #####

reddit = praw.Reddit(
    client_id=app_client_id,
    client_secret=app_secret,
    user_agent=username,
)

# Set the subreddit and keyword
subrdt_df = pd.read_csv("data/subreddits.csv")
subreddits_list = list(subrdt_df["subreddit_tag"])

#### Generate glossary lists
nasa_glossary = pd.read_csv("data/glossaries/nasa_glossary.csv")
davis_glossary = pd.read_csv("data/glossaries/davis_glossary.csv")
epa_glossary = pd.read_csv("data/glossaries/epa_glossary.csv")
glossaries = [nasa_glossary, davis_glossary, epa_glossary]


def generate_glossary_types(glossary):
    clean = [keyword.lower() for keyword in glossary]
    return glossary, clean


def get_posts_from_glossaries(glossary):
    unclean_keywords, clean_keywords = generate_glossary_types(glossary)
    matching_posts = []
    for subred in subreddits_list:
        subreddit = reddit.subreddit(subred)
        found_count = 0
        for post in subreddit.search(query=' OR '.join(unclean_keywords + clean_keywords), time_filter='all'):
            print(post.title)
            found_count += 1
            matching_posts.append([post.id, post.subreddit.display_name, post.title, post.author.name, post.url, post.selftext, post.score, post.num_comments, post.created_utc])

    # Convert matching_posts list into a pandas dataframe
    cols = ['id', 'subreddit', 'title', 'author', 'url', 'selftext', 'score', 'num_comments', 'created_utc']
    matching_posts_df = pd.DataFrame(matching_posts, columns=cols)
    
    return matching_posts_df



# epa_data = get_posts_from_glossaries(epa_glossary)
# print(epa_data.head())
# print(epa_data.shape)
# print(epa_data.shape)
# nasa_data = get_posts_from_glossaries(nasa_glossary)
# print(nasa_data.head())
# print(nasa_data.shape)
# davis_data = get_posts_from_glossaries(davis_glossary)
# print(davis_data.head())
# print(davis_data.shape)

# all_data = pd.concat([epa_data, nasa_data, davis_data])

# # get only the unique rows that have a unique entry for the id column

# all_data = all_data.drop_duplicates(subset=['id'])

# print(all_data.shape)
# print(all_data.head())

# # save the data to a csv file

# all_data.to_csv("data/raw_data/raw_politcal_posts_two.csv", index=False)



##### Getting mock truth and fake labels #####

def get_posts_from_one(glossary,subred):
    unclean_keywords, clean_keywords = generate_glossary_types(glossary)
    matching_posts = []
    subreddit = reddit.subreddit(subred)
    found_count = 0
    for post in subreddit.search(query=' OR '.join(unclean_keywords + clean_keywords), time_filter='all'):
        print(post.title)
        found_count += 1
        matching_posts.append([post.id, post.subreddit.display_name, post.title, post.author.name, post.url, post.selftext, post.score, post.num_comments, post.created_utc])

    # Convert matching_posts list into a pandas dataframe
    cols = ['id', 'subreddit', 'title', 'author', 'url', 'selftext', 'score', 'num_comments', 'created_utc']
    matching_posts_df = pd.DataFrame(matching_posts, columns=cols)
    
    return matching_posts_df

skeptics_data = get_posts_from_one(epa_glossary,'climateskeptics')
print(skeptics_data.head())
print(skeptics_data.shape)


scientists_data = get_posts_from_one(epa_glossary,'climate_science')
print(scientists_data.head())
print(scientists_data.shape)


#save 
skeptics_data.to_csv("data/raw_data/skeptics_data.csv", index=False)
scientists_data.to_csv("data/raw_data/scientists_data.csv", index=False)
#### Requesting data ####



#### Cleaning the data ####'


def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def clean_body(df):

    print("this is the body before cleaning", df['body'])

    #removing unecessary space
    df['body'] = df['body'].apply(lambda x: " ".join(x.split()))

    # make all text lowercase
    df['body'] = df['body'].apply(lambda x: x.lower())

    # remove punctuation
    df['body'] = df['body'].apply(lambda x: re.sub('[^a-zA-Z0-9\s]', '', x))
    print(list(df['body']))

    #remove emojis
    df['body'] = df['body'].apply(lambda x: remove_emojis(x))

    #saving the clean data
    return df



