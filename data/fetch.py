import requests
import requests.auth
import pandas as pd


#### Requesting a token ####
# NOTE: This requests a token, which should work for more than one call, for security reasons the password is not on display, but if you need to request ask Livia

# username = "project-user"
# password = ""
# app_client_id = "dyczxLp57fVfQrBb4epVQA"
# app_secret = "CEpQfSvjR0aJ2-0deD7xyEvIv4uF5A"

# client_auth = requests.auth.HTTPBasicAuth(app_client_id, app_secret)
# post_data = {"grant_type": "password", "username": username, "password": password}
# headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}

# response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
# TOKEN = response.json()['access_token']


#### Response received ####

TOKEN = '26658734656586-7GRT_v-Ehz000K0xuX3tEupSWSY9ig'
print(TOKEN)


#### Requesting data ####


###### This section has the code that just gets the posts for subreddits where key words don't need to be searched for ####
headers = {"Authorization": "bearer 26658734656586-2gMR6jRsCRQX8Qm_bNzvpb8wcjBNuQ", "User-Agent": "'your bot 0.1"}

#### First just working with all the post climate skeptics data ####
url = f"https://api.pushshift.io/reddit/submission/search/?subreddit=climateskeptics"

# Create an empty list to hold all the posts


def get_subreddit_posts(url):
    
    params = {"size": 1000}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        #throw an error if the request fails
        raise Exception(response.status_code, response.text)
    data = response.json()["data"]

    all_posts = []
    for post in data:
            post_data = {
                "title": post["title"],
                "author": post["author"],
                "body": post["selftext"],
                "created_utc": post["created_utc"],
                "score": post["score"],
                "num_comments": post["num_comments"],
                "subreddit": post["subreddit"]
            }
            all_posts.append(post_data)
    df = pd.DataFrame(all_posts)
    print(df.head())
    return df

subreddit = ["climateskeptics"]
#save to csv
def get_all_of_subreddit(subreddit_lst):
    all= []
    for subredit in subreddit_lst:
        url = f"https://api.pushshift.io/reddit/submission/search/?subreddit={subredit}"
        df = get_subreddit_posts(url)
        all.append(df)
    all_dfs = pd.concat(all)
    all_dfs.to_csv("data/all_subreddits.csv", index=False)
    return all_dfs

result = get_all_of_subreddit(subreddit)
print(result.head())
    
   


### Expand the code for getting the data with the search for specific subreddits #

# These are the subreddits that we want to use: 