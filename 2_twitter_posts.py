import twint
import string
import re, datetime,gensim,spacy
import pandas as pd, numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt 
from collections import Counter
from textblob import TextBlob
from nltk.corpus import wordnet
from gensim.models import CoherenceModel, LdaModel, LsiModel, HdpModel,Phrases
from gensim.corpora import Dictionary
from nltk.tokenize import TweetTokenizer 
from nltk.corpus import stopwords, words 
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
from gensim.utils import simple_preprocess
from symspellpy.symspellpy import SymSpell, Verbosity
from gensim.models.phrases import Phrases, Phraser
import warnings
warnings.filterwarnings("ignore")
#############################################################
words_english = words.words()

## Define Functions #######
def make_bigrams(texts):
	return [bigram_mod[doc] for doc in texts]
def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
##################################
x = input('Enter a specific keyword: ')

title = input('Enter a title name for your csv file (do not use space): ')

"""while True:
	y = input('Please enter Limit to be scrapped: ')
	try:
		y = int(y)
		if y > 10000:
			print('Too many defualting to 10,000')
			y =  int(10000)
		else:
			y = y

		break
	except (ValueError):
		print('Please choose a number.')"""

while True:
	try:
		since = input('Please choose date since (YYYY-MM-DD): ')
		since = str(since)
		datetime.datetime.strptime(since, '%Y-%m-%d')
		break
	except (ValueError):
		print('Please choose date since (YYYY-MM-DD format): ')

while True:
	try:
		until = input('Please choose date until (YYYY-MM-DD): ')
		until = str(until)
		datetime.datetime.strptime(until, '%Y-%m-%d')
		break
	except (ValueError):
		print('Please choose date until (YYYY-MM-DD format): ')
"""while True:
	z = input('Please the number of topics you expect to model: ')
	try:
		z = int(z)
		if z > 10:
			print('Too many topics defaulting to 10')
			z =  int(10)
		else:
			z = z

		break
	except (ValueError):
		print('Please choose a number.')"""

c = twint.Config()
#for i in x:
c.Search= str(x)
print('here')
c.Store_csv = True
c.Lang = "en"
# CSV Fieldnames
c.Format = "Tweets: {tweet} | Username: {username} | Likes: {likes} | RTs: {retweets}"
#c.Limit = y #use the parameter y above if number of tweets is the major constraints
c.Since = since
c.Until = until

c.Output = str(title)+".csv"
twint.run.Search(c)

raw_data = pd.read_csv(str(title)+".csv")
twitter = raw_data.drop_duplicates()


fav_max = np.max(twitter['likes'])
rt_max  = np.max(twitter['retweets'])

fav = twitter[twitter.likes == fav_max].index[0]
rt  = twitter[twitter.retweets == rt_max].index[0]

# Max FAVs:
print("The tweet with more likes is: \n{}".format(twitter['tweet'][fav]))
most_liked = [twitter['tweet'][fav]]
print("Number of likes: {}".format(fav_max))
liked = [fav_max]
print("Posted by: {}".format(twitter['username'][fav]))
posted = [twitter['username'][fav]]

# Max RTs:
print("The tweet with more retweets is: \n{}".format(twitter['tweet'][rt]))
most_retweet = [twitter['tweet'][rt]]
print("Number of retweets: {}".format(rt_max))
retweeted = [rt_max]
print("Posted by: {}".format(twitter['username'][rt]))
rt_posted = [rt]

pd.DataFrame({'Most Liked':most_liked,'Number of Likes':liked,'Username':posted, 'most retweeted':most_retweet,'number of retweet':retweeted, 'Origin Username':rt_posted})

# Time Series for number of FAVs & RTs:
tfav = pd.Series(twitter['likes'].values, index=twitter['time'])
tret = pd.Series(twitter['retweets'].values, index=twitter['time'])

tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret.plot(figsize=(16,4), label="Retweets", legend=True)
plt.savefig('twitter_time_series.png', format='png', dpi=300)

twitter['SA'] = np.array([ analize_sentiment(tweet) for tweet in twitter['tweet'] ])

pos_tweets = int(len(twitter.loc[twitter.SA > 0]))
neu_tweets = int(len(twitter.loc[twitter.SA == 0]))
neg_tweets = int(len(twitter.loc[twitter.SA < 0]))

print("Percentage of positive tweets: {}%".format(pos_tweets*100/len(twitter['tweet'])))
print("Percentage of neutral tweets: {}%".format(neu_tweets*100/len(twitter['tweet'])))
print("Percentage of negative tweets: {}%".format(neg_tweets*100/len(twitter['tweet'])))
sentiment_count = pd.DataFrame({'%Positive':[pos_tweets*100/len(twitter['tweet'])],'%Neutral':[neu_tweets*100/len(twitter['tweet'])],'%Negative':[neg_tweets*100/len(twitter['tweet'])]})

sentiment_count.to_csv('%twitter%_sentiment_count.csv',index=False)
###########################################
extension = []
stop_words = stopwords.words('english')
extended_words = x.split(" ")
for i in extended_words:
	extension.append(i)
stop_words.extend(extension)
extension.append('hotel')
extension.append('shangri_la')
extension.append('shangri')
extension.append('la')
extension.append('pic')
extension.append('twitter')
extension.append('com')
extension.append(' com')
extension.append('vol')
stop_words.extend(extension)
data=twitter.tweet.values.tolist()
data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
data = [re.sub('\s+', ' ', sent) for sent in data]
data = [re.sub("\'", "", sent) for sent in data]
# remove stock market tickers like $GE
data = [re.sub(r'\$\w*', '', sent)for sent in data]
# remove old style retweet text "RT"
data = [re.sub(r'^RT[\s]+', '', sent)for sent in data]
# remove hyperlinks
data = [re.sub(r'https?:\/\/.*[\r\n]*', '', sent)for sent in data]
# remove hashtags
# only removing the hash # sign from the word
data = [re.sub(r'#', '', sent)for sent in data]
# remove @users
data = [re.sub(r'@[\w]*', '', sent)for sent in data]

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

data_words = list(sent_to_words(data))

bigram = gensim.models.Phrases(data_words, min_count=5, threshold=5) # higher threshold fewer phrases. 

bigram_mod = gensim.models.phrases.Phraser(bigram)

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

data_words_nostops = remove_stopwords(data_words)


data_words_bigrams = make_bigrams(data_words_nostops)


# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN'])#, 'ADJ'])#, 'VERB']#, 'ADV'])

id2word = Dictionary(data_lemmatized)

texts = data_lemmatized

corpus = [id2word.doc2bow(text) for text in texts]

goodLdaModel = LdaModel(corpus=corpus, id2word=id2word, iterations=100000, num_topics=1) #use the parameter z for a more dynamic topic models
words = []
for t in range(goodLdaModel.num_topics):
	print (goodLdaModel.show_topic(t))
	words.append([str(k) for k,v in goodLdaModel.show_topic(t)])
	#print('Printing for Topic ' + str(t)) 
	plt.figure()
	plt.imshow(WordCloud().generate(" ".join([str(k) for k,v in goodLdaModel.show_topic(t)])))
	plt.axis("off")
	plt.title("Topic #" + str(t))
	plt.savefig(str(t)+'.png', format = 'png', dpi=300)
	plt.close()

word = []
words = remove_stopwords(words)
for i in words:
	for j in i:
		word.append(j)
semantic = []
pos = []
neu = []
neg = []

print(word)
for i in word:
	semantic.append(i)
	positive = twitter.loc[twitter['SA']>0]
	pos.append(positive.tweet.str.count(i).sum())
	neutral = twitter.loc[twitter['SA']==0]
	neu.append(neutral.tweet.str.count(i).sum())
	negative = twitter.loc[twitter['SA']<0]
	neg.append(negative.tweet.str.count(i).sum())

semantic_mention = pd.DataFrame({'word':semantic,'Positive Mention':pos,'Neutral Mention':neu, 'Negative Mention':neg})
#semantic_mention = semantic_mention.loc[(semantic_mention['Positive Mention']!=0)&(semantic_mention['Neutral Mention']!=0)&(semantic_mention['Negative Mention']!=0)]
semantic_mention.to_csv('%twitter%_semantic_mention.csv', index=False)
