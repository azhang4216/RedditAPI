# Reddit-Twitter API 🐦

This is a project that uses tweepy and praw APIs to tweet out the top-rated (hottest) memes onto a twitter account.
During quarantine, I wanted to make something that could uplift people and make people smile. And I thought that memes are a great universal connector for laughter and joy, so I wanted to bring quality memes to more people on different social media platforms using this project.
The twitter handle is: @RedditFunniest, or, you can access the Twitter page via: https://twitter.com/RedditFunniest.

## Getting Started 🚀

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites 💻

For this project to run, you will need to install praw, tweepy, and python-dotenv packages.
These packages can be installed by going to Settings/Preferences > Interpreter Settings. 
From there, click the "+" button and search for those packages in the search bar, and install. 

### Installing 

In order to run the code yourself, you must put in your own access codes, ie:
* Reddit client ID
* Reddit client Secret
* Reddit user agent
* Reddit account username
* Reddit account password

* Twitter account username
* Twitter account password
* Twitter consumer key
* Twitter consumer secret
* Twitter access token
* Twitter secret access token

If you do not have any of these keys or need help signing up for your own API keys, please visit the following links for guideline:
https://docs.inboundnow.com/guide/create-twitter-application/

## Implementation Explained

The tests are relatively straightforward: every time you run the code, a new tweet should pop up in the twitter handle citing the reddit meme's caption and creditting the author. 
You can specify from which subreddit you would like to pull from by going to line 59 and changing the string parameter to the desired subreddit you would like to tweet your meme from. In my case, I put:

```
subreddit = reddit.subreddit("WholesomeMemes") 
```

The API then takes the "hottest" rated meme from your specified subreddit and checks if it has already been posted (using the posted_url.txt to keep check). Then, the hottest meme that has not been posted on the account will be tweeted out. 

Note: GIF format media is not supported, and neither are videos. Only images (our goal is memes). This means the code will skip over any videos or gifs, and get the next "hottest" meme from the subreddit.

## Running the tests

You can check if everything is running smoothly by going to https://twitter.com/RedditFunniest and refreshing to see if the tweet pops up, like so:

![](Images/Successful_Tweet.png)

If everything works, you should be able to run the code, and see in your console "meme tweeted" followed by exit code 0. 

To check if it tweeted from your subreddit, and tweeted from the hottest criteria, check the subreddit page for your indicated subreddit to see if the redditer name, caption, and meme image match. If they do, then it's a success! Here is what it should look like (I used the r/WholesomeMemes subreddit):

![](Images/Matches_Reddit.png)

Note that if the program works correctly, the "stickied" post(s) at the top (messages by admin) are not added.

## Acknowledgments 🙏

I consulted these following sources for help on my project (they are also credited in the comments of my main API.py):

* PyMoondra
* Reddit API description page
* Twitter API Developer Info Page
* https://stackoverflow.com/questions/31748444/how-to-update-twitter-status-with-image-using-image-url-in-tweepy
* https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
