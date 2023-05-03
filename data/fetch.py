import requests
import requests.auth
import pandas as pd
import re
import nltk
import praw
import asyncio
import datetime
from psaw import PushshiftAPI



#### Info for fetching  ####

username = "project-user"
app_client_id = "dyczxLp57fVfQrBb4epVQA"
app_secret = "CEpQfSvjR0aJ2-0deD7xyEvIv4uF5A"

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


############ Getting posts from one posts ############




def get_all_posts(subred):

    subreddit = reddit.subreddit(subred)

    # Change to hot, top, new
    posts = subreddit.new(limit = None)
    
    posts_dict = {"title": [], "selftext": [],
                "id": [], "score": [], "upvote_ratio": [],
                "num_comments": [],"created_utc":[]
                }

    ## Starts at 2018-2023
    start_date = '01-01-15 00:00:00'
    start_date = datetime.datetime.strptime(start_date, '%d-%m-%y %H:%M:%S').timestamp()

    for post in posts:
        # Date of each posts' creation
        date = post.created_utc
        if date > start_date:
            # Title of each post
            posts_dict["title"].append(post.title)
        
            # Text inside a post
            posts_dict["selftext"].append(post.selftext)
        
            # Unique ID of each post
            posts_dict["id"].append(post.id)
        
            # The score of a post
            posts_dict["score"].append(post.score)
            
            # Upvote Ratio of a post
            posts_dict["upvote_ratio"].append(post.upvote_ratio)
        
            # Total number of comments inside the post
            posts_dict["num_comments"].append(post.num_comments)
            
            # Date the post was Created
            posts_dict["created_utc"].append(post.created_utc)
            
        
          
    # Saving the data in a pandas dataframe
    all_posts = pd.DataFrame(posts_dict)

    return all_posts


# uncomment 
#climate_skeptics = get_all_posts("climateskeptics")
#climate_skeptics.to_csv("data/raw_data/climate_skeptics_three.csv", index=False)



climate_science = get_all_posts("climate_science")
print(climate_science.shape)
climate_science.to_csv("data/raw_data/climate_science_three.csv", index=False)









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



