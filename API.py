'''
Reddit-Twitter API that posts best memes based on score
Credits the author and includes title
Author: Angela Zhang
Date: May 15, 2020
Sources Consulted: PyMoondra, Reddit API description page,
Twitter API Developer Info Page, https://stackoverflow.com/questions/31748444/how-to-update-twitter-status-with-image-using-image-url-in-tweepy
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
Packages installed: praw, tweepy
'''
import praw
import tweepy
import requests
import os

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

supported = ["jpg", "png", "jpeg"]

# creates and returns reddit object
def login_reddit():
    try:
        red = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         user_agent=user_agent, username=r_username, password=r_password)
        return red

    except Exception as e:
        print("Failed to log into Reddit. Make sure Reddit credentials are valid.")
        return None

# creates and returns twitter object
def login_twitter():
    try:
        twit = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
        twit.set_access_token(access_token, access_token_secret)
        return twit

    except Exception as e:
        print("Failed to log into Twitter. Make sure Twitter credentials are valid.")
        return None

def tweet_meme():
    # creates reddit and subreddit objects
    reddit = login_reddit()
    if reddit == None:
        return
    try:
        subreddit = reddit.subreddit("WholesomeMemes") # wholesome meme subreddit, can change to desired subreddit
    except Exception as e:
        print("We can't find that subreddit. Please try again, and check if the subreddit is accessible to your account.")

    # creates twitter objects
    twitter = login_twitter()
    if twitter == None:
        return
    t_api = tweepy.API(twitter)

    # filters posts based on hotness
    hot = subreddit.hot(limit=50)

    message = ""

    for submission in hot:
        # checks if it is a "stickied" post, has been posted, and is a supported format for posting
        if not submission.stickied and not check_if_string_in_file(submission.url) and is_supported(submission.url):
            # makes a message and breaks when criteria met
            message = '\"' + submission.title + '\"' + ' post by ' + str(submission.author)
            break

    print(submission.name)

    if message == "":
        print("Sorry, too many memes from this reddit posted, or the posts are not supported.")
        return

    # creates an appropriate file for the meme image to come
    meme_image = 'temp.jpg'

    request = requests.get(submission.url, stream=True)
    # print(submission.url)

    # checks if request code is valid and if submission url was successfully a new one
    if request.status_code == 200:
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
    for format in supported:
        if url.endswith(format):
            return True
    return False

tweet_meme()

# run for continuous tweeting (not recommended for spam reasons)
'''while True:
   tweet_meme()
   time.sleep(10)'''

