"""
HESAM MOTLAGH - The Johns Hopkins Univeristy - Hesamnmotlagh@gmail.com
-------------------------------------------------------------------------------
Script name:     analyze_twitter_sentiment
First written:   2015.07.17
Last edited:     2015.07.20

Purpose:
The script was written by Hesam Motlagh for the Data Incubator Semi-finals challenge.
A portion of this script is based off of a web-post I found online
(link = http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/)
but I have hacked it to work for my purposes - i.e. to take in tweets about
stocks (using ticker symbols as the search criterion) and then analyze their
sentiment.  From there I will see if it correlates/predicts stock market 
movements.
"""
#import classes to be used
import argparse, urllib, json, os, oauth2, time, re, string, nltk


#cleanTweet will clean up the tweet and also make the data ready for analysis
#this is a hacked version of a script I found online
stopWords, featureList = [], []
def cleanTweet(tweet):
    tweet = tweet.lower() #make all lower case
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet) #Convert www.* or https?://* to URL
    tweet = re.sub('@[^\s]+','AT_USER',tweet) #change @username to AT_USER
    tweet = re.sub('[\s]+', ' ', tweet) #remove excess white space
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #replace hashtag
    tweet = tweet.strip('\'"') #remove all instances of "\"
    tweet = tweet.strip(',') #remove all instances of commas 
    return tweet

#replace mutlti will remove multiple repitions of characters    
def replaceMulti(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

#the point of this function is to get all the stop words that have no meaning
#or contribution to sentiment.  
def getStopWords(stopWordListFileName):
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
    
#this will generate the feature vector that I will use to for the Naive-Bayes
#machine-learning algorithm.
def getFeatureVector(tweet):
    featureVector = []
    words = tweet.split() #this will break it down into words
    for w in words:
        w = replaceMulti(w) #see above function
        w = w.strip('\'"?,.') #remove punctuation
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w) #check if tweet starts with alphabet
        if(w in stopWords or val is None): #ignore it if it's a stop word
            continue
        else:
            featureVector.append(w.lower())
    return featureVector #sent the feature vector back
    
#this function will take a tweet and return back the features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features



#first let's take in the training data set and generate feature words for each
#tweet
print "Reading in training data"
raw = open('training_set.csv','r') #this was a training set I obtained online
#from a blog post - it contains millions of analyzed tweets for sentiment
#link = http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip
lines = raw.readlines() #read in the lines
raw.close() #close the file
train_dat = []
stop_words = getStopWords('stop_words.txt') #get the stop words of interest
for line in lines[1:len(lines)]: #now go through and extract all the feature vectors along with their sentiment
    feat_vec = getFeatureVector(cleanTweet(line0.split(',')[3]))
    if(int(line.split(',')[1]) == 0): #check if it's a negative sentiment
        train_dat.append([feat_vec,'negative'])
    else:
        train_dat.append([feat_vec,'positive']) #check if it's a positive sentiment
    featureList.extend(feat_vec)
print "Done" 
print "Performing machine learning training"
featureList = list(set(featureList))  
#I am about to perform a Naive-Bayes ML algorithm - this will then be used
#to analyze all the tweets I have downloaded from the twitter API
train_set = nltk.classify.util.apply_features(extract_features, train_dat)
NBclassify = nltk.NaiveBayesClassifier.train(train_set)
print "Done"
#now we can classify tweets
print "Reading in twitter data"
raw = open('AAPL_Tweets_Seg1.dat','r')
tweets = raw.readlines()
raw.close()
print "Done"
print "Analyzing Twitter data"
outfile = open('AAPL_twitter_sent.dat','w')
#ok now go through all the tweets and classify them according to our
#NB-machine learning algorith
for tweet in tweets:
    clean_tweet = cleanTweet(tweet.split(',')[1]) + "\n"
    output = NBclassify.classify(extract_features(getFeatureVector(clean_tweet)))
    if(output == 'positive'):
        outfile.write(tweet.split(',')[0] + ", 1.0" + "\n")
    else:
        outfile.write(tweet.split(',')[0] + ", 0.0" + "\n")


outfile.close()
print "Done!!!"

