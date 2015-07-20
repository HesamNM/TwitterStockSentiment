"""
HESAM MOTLAGH - The Johns Hopkins Univeristy - Hesamnmotlagh@gmail.com
-------------------------------------------------------------------------------
Script name:     get_twitter_data.py
First written:   2015.07.13
Last edited:     2015.07.17

Purpose:
The script was written by Hesam Motlagh for the Data Incubator Semi-finals challenge.
This is a hacked version of a script I found online to download twitter data
(link = http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/)
This will search for tweets with certain ticker symbols and download all of them
via the API
"""
import argparse, urllib, json, os, oauth2, time, re, string


class TweetData:
    #get_config will find the config.json file in the PWD and get the proper
    #consumer/access keys to authenticate with the twitter API
    def get_config(self):
        config = {}
        if os.path.exists('config.json'):
            with open('config.json') as f:
                config.update(json.load(f))
        else:
           print "ERROR: The configuration file is not present in the PWD"
        return config

    #this is the OAUTH2 request that will put together the proper tokens I
    #need (consumer/client) to interact with the Twitter API
    def oauth_req(self, url, http_method="GET", post_body=None,
                  http_headers=None):
        config = self.get_config()
        consumer = oauth2.Consumer(key=config.get('consumer_key'), \
        secret=config.get('consumer_secret'))
        token = oauth2.Token(key=config.get('access_token'), \
        secret=config.get('access_token_secret'))
        client = oauth2.Client(consumer, token)

        resp, content = client.request(
            url,
            method=http_method,
            body=post_body or '',
            headers=http_headers
        )
        return content
    

    #getData will request the tweets from the twitter API
    def getData(self, keyword, max_id):
        maxTweets = 100 #can only get 100 tweets at a time :-(
        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        if(max_id == -1):  #if it's the first search we'll just start with the most recent
            data = {'q': keyword, 'lang': 'en', 'result_type': 'recent', \
            'count': maxTweets, 'include_entities': 0}
        else: data = {'q': keyword, 'lang': 'en', 'result_type': 'recent', \
        'count': maxTweets, 'include_entities': 0,'max_id': max_id}
        #otherwise, we'll start from where we left off
        url += urllib.urlencode(data) #encode our parameters
        response = self.oauth_req(url) #request via oauth2 
        return json.loads(response) #return the data!
        
#cleanTweet will clean up the tweet and also make the data ready for analysis
#this is a hacked version of a script I found online
def cleanTweet(tweet):
    tweet = tweet.lower() #make all lower case
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet) #Convert www.* or https?://* to URL
    tweet = re.sub('@[^\s]+','AT_USER',tweet) #change @username to AT_USER
    tweet = re.sub('[\s]+', ' ', tweet) #remove excess white space
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #replace hashtag
    tweet = tweet.strip('\'"') #remove all instances of "\"
    tweet = tweet.strip(',') #remove all instances of commas 
    return tweet


#output file name 
filename = "AAPL_Tweets_Seg1.dat"
ticker = "AAPL"

#collect the first batch of tweets starting with the most recent and then
#move back in time from there
tweet_set = TweetData()
json_to_write = tweet_set.getData(ticker,-1)
output = open(filename,'w')
max_id = json_to_write['statuses'][len(json_to_write['statuses'])-1]['id']
for tweet in json_to_write['statuses']:
    output.write(str(tweet['created_at'][4:len(tweet['created_at'])]).strip(',')\
    +","+cleanTweet(str((tweet['text']).encode('utf-8',"ignore")))+"\n")
    #output the data above to the output file.  All that extra code is to deal
    #with the text formatting to make it easier to process for the machine-learning
    #algorithm.


output.close()
#ok, now I will go through all the tweets going back in time until I get an error
#which means I have moved back in time more than Twitter will allow me to
for i in range(1,100000):
    time.sleep(5.1) #Wait for at least 5.0 seconds to not overload the API
    output = open(filename,'a')
    json_to_write = tweet_set.getData(ticker,max_id)
    max_id = json_to_write['statuses'][len(json_to_write['statuses'])-1]['id']
    date = json_to_write['statuses'][len(json_to_write['statuses'])-1]['created_at']
    print "Max ID = " + str(max_id)
    print "Date   = " + str(date)
    for tweet in json_to_write['statuses']:
        output.write(str(tweet['created_at'][4:len(tweet['created_at'])]).strip(',')\
    +","+cleanTweet(str((tweet['text']).encode('utf-8',"ignore")))+"\n")
    output.close()
    
