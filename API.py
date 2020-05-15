'''
Reddit-Twitter API that posts best memes based on score
Credits the author and includes title
Author: Angela Zhang
Date: May 15, 2020
Sources Consulted: PyMoondra, Reddit API description page,
Twitter API Developer Info Page, https://stackoverflow.com/questions/31748444/how-to-update-twitter-status-with-image-using-image-url-in-tweepy
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
Packages installed: praw, tweepy, python-dotenv
'''
import praw
import tweepy
import requests
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Accessing variables from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
user_agent = os.environ.get('USER_AGENT')
r_username = os.environ.get('R_USERNAME')
r_password = os.environ.get('R_PASSWORD')

t_username = os.environ.get('T_USERNAME')
t_password = os.environ.get('T_PASSWORD')
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# creates and returns reddit object
def login_reddit():
    try:
        red = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         user_agent=user_agent, username=r_username, password=r_password)
        return red

    except Exception as e:
        return None

# creates and returns twitter object
def login_twitter():
    try:
        twit = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
        twit.set_access_token(access_token, access_token_secret)
        return twit

    except Exception as e:
        return None

def tweet_meme():
    # creates reddit and subreddit objects
    reddit = login_reddit()
    subreddit = reddit.subreddit("WholesomeMemes") # wholesome meme subreddit, can change to desired subreddit

    # creates twitter objects
    twitter = login_twitter()
    t_api = tweepy.API(twitter)

    # filters posts based on hotness
    hot = subreddit.hot(limit=50)

    for submission in hot:
        # checks if it is a "stickied" post, has been posted, and is a supported format for posting
        if not submission.stickied and not check_if_string_in_file(submission.url) and is_supported(submission.url):
            # makes a message and breaks when criteria met
            message = '\"' + submission.title + '\"' + ' post by ' + str(submission.author)
            break

    # creates a jpg file for the meme image to come
    meme_image = 'temp.jpg'

    request = requests.get(submission.url, stream=True)
    # print(submission.url)

    # checks if request code is valid and if submission url was successfully a new one
    if request.status_code == 200 and (not check_if_string_in_file(submission.url)):
        # keeps track of tweeting out of submission in posted_url.txt
        modify_visited(submission.url)

        # tweets out with message and image
        with open(meme_image, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        t_api.update_with_media(meme_image, message)
        os.remove(meme_image)

        print("meme tweeted")
    else:
        # may occur due to either request failure or having tweeted too many memes (out of limit 50)
        print("unable to tweet meme")

# helper functions
# checks if any line in the posted_url.txt contains given url
def check_if_string_in_file(url):
    # Open the file in read only mode
    with open("posted_url.txt", 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if url in line:
                return True
    return False

# adds url of newly tweeted image if it was successfully tweeted
def modify_visited(url):
    with open("posted_url.txt", 'a') as write_obj:
        write_obj.write("\n" + url)

# checks if url of image is a supported format for tweeting
def is_supported(url):
    # videos (unsupported) do not have a "." as the 4th last character in their url
    if url[-4] != "." or is_gif(url):
        return False
    return True

# helper function to is_supported(url) that checks if image is gif (unsupported)
def is_gif(url):
    if url[-3] == "g" and url[-2]== "i" and url[-1] == "f":
        return True
    return False

tweet_meme()

# run for continuous tweeting (not recommended for spam reasons)
'''while True:
   tweet_meme()
   time.sleep(10)'''

