from flask import Flask, request
import json
from datetime import datetime, timedelta
from twitter import *
from textblob import TextBlob

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re, string, requests
import nltk
# nltk.download('words', 'stopwords')



t = Twitter(auth = OAuth('845923993290887170-amXsT3U6aaHw5cJx3Mg5zQ0cbpJt0tz', 
        				'Po250EXxr2Hs1EOCZ22vyMWRlPBH3YzVBlUn8wxQw9sgY', 
        				't32qWI29icsvpny9Uh4cs3dHQ', 
        				'ovemYqKnfLeSFPF3epXPf1A0ZWKQnCdFAwPuLwBiL5golu4MrS'))


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
	start_time = request.args.get('start_time', None)
	end_time   = request.args.get('end_time'  , None)

	try:
		start_time = datetime.strptime(start_time, "%Y-%m-%d")
		end_time   = datetime.strptime(end_time,   "%Y-%m-%d")
		if start_time >= end_time: raise Exception
	except Exception as e:
		start_time = datetime.now() - timedelta(days=30)
		end_time   = datetime.now()

	tweets = get_tweets("tttaaa")

	aggregated_satisfied = []
	aggregated_neutral = []
	aggregated_angry = []

	for tweet in tweets:
		tatta = tweet['text']
		print tatta
		tweet = clean_tweet(tweet['text'])
		blob = TextBlob(tweet)
		polarity = blob.sentiment.polarity
		if polarity > 0:
			aggregated_satisfied.append(tatta)
		elif polarity == 0:
			aggregated_neutral.append(tatta)
		else:
			aggregated_angry.append(tatta)



	aggregated_data = {}
	aggregated_data['angry']     = {'count':len(aggregated_angry), 'tweets': aggregated_angry}
	aggregated_data['neutral']   = {'count':len(aggregated_neutral), 'tweets': aggregated_neutral}
	aggregated_data['satisfied'] = {'count':len(aggregated_satisfied), 'tweets': aggregated_satisfied}

	headers = {'content-type': 'application/json'}
	response = requests.post('http://192.168.106.128:3000/', data=json.dumps(aggregated_data), headers=headers)
	print type(response.content)


	return json.dumps(aggregated_data)



def get_tweets(search_terms):
	tweets = []
	response = t.search.tweets(q="#october", count=10, result_type='recent')
	for status in response['statuses']:
		data = {'user': status['user'], 'text':status['text']}
		tweets.append(data)
	return tweets


def clean_tweet(tweet):
	english_vocab = set(w.lower() for w in nltk.corpus.words.words())
	if tweet.startswith('@null'):
	   return "[Tweet not available]"
	tweet = re.sub(r'\$\w*','',tweet) # Remove tickers
	tweet = re.sub(r'https?:\/\/.*\/\w*','',tweet) # Remove hyperlinks
	tweet = re.sub(r'['+string.punctuation+']+', ' ',tweet) # Remove puncutations like 's
	twtok = TweetTokenizer(strip_handles=True, reduce_len=True)
	tokens = twtok.tokenize(tweet)
	stop = stopwords.words('english')
	tokens = [i.lower() for i in tokens if i not in stop and len(i) > 2 and i in english_vocab]
	return " ".join(tokens)




