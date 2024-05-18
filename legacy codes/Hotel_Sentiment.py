import string, nltk, os, glob, pickle
from bs4 import BeautifulSoup
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
from nltk.corpus import stopwords, words 
from nltk.stem import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from gensim.utils import simple_preprocess
from symspellpy.symspellpy import SymSpell, Verbosity
from gensim.models.phrases import Phrases, Phraser
import warnings
warnings.filterwarnings("ignore")
from sklearn.externals import joblib
#############################################################
words_english = words.words()
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
sid = SentimentIntensityAnalyzer() # for VADER SA
## Define Functions #######
def make_bigrams(texts):
	return [bigram_mod[doc] for doc in texts]

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwords from text
    return text

def analyze_sentiment(text):
    '''
    Utility function to classify the polarity of a text
    using VADER.
    '''
    # Analyze sentiment using VADER
    scores = sid.polarity_scores(text)
    
    # Classify the sentiment
    if scores['compound'] >= 0.05:
        return 1  # Positive
    elif scores['compound'] <= -0.05:
        return -1  # Negative
    else:
        return 0  # Neutral


# def analyze_sentiment(text):
#     '''
#     Utility function to classify the polarity of a text
#     using textblob.
#     '''
#     analysis = TextBlob(clean_text(text))
#     if analysis.sentiment.polarity > 0:
#         return 1
#     elif analysis.sentiment.polarity == 0:
#         return 0
#     else:
#         return -1
# ##################################
# arr = os.listdir()
# csv_files = []
# for i in arr:
# 	if i[-4:] == '.csv':
# 		csv_files.append(i)
# 	else:
# 		continue
# trip_advisor = []
# agoda = []
# booking = []
# extension = []
# for i in csv_files:
# 	for j in (i[:-4].split(" ")):
# 		extension.append(j.lower())
# 		if j == "tripadvisor":
# 			trip_advisor.append(i)
# 		elif j == "AGODA":
# 			agoda.append(i)
# 		elif j == "BOOKING.COM":
# 			booking.append(i)
# 		else:
# 			continue

# for i in trip_advisor:
# 	print(i)
# 	tripadvisor = pd.read_csv(str(i))
# 	tripadvisor = tripadvisor.replace(np.nan, '', regex=True)
# 	tripadvisor['comments']=tripadvisor['comments'].dropna()
# 	tripadvisor['SA'] = np.array([ analyze_sentiment(comments) for comments in tripadvisor['comments'] ])

# 	pos_texts = int(len(tripadvisor.loc[tripadvisor.SA > 0]))
# 	neu_texts = int(len(tripadvisor.loc[tripadvisor.SA == 0]))
# 	neg_texts = int(len(tripadvisor.loc[tripadvisor.SA < 0]))

# 	print("Percentage of Positive Reviews: {}%".format(pos_texts*100/len(tripadvisor['SA'])))
# 	print("Percentage of Neutral Reviews: {}%".format(neu_texts*100/len(tripadvisor['SA'])))
# 	print("Percentage of Negative Reviews: {}%".format(neg_texts*100/len(tripadvisor['SA'])))
# 	sentiment_count = pd.DataFrame({'%Positive':[pos_texts*100/len(tripadvisor['SA'])],'%Neutral':[neu_texts*100/len(tripadvisor['SA'])],'%Negative':[ neg_texts*100/len(tripadvisor['SA'])]})
# 	print(sentiment_count.head(5))
# 	sentiment_count.to_csv('%tripadvisor%_sentiment_count.csv',index=False)
# 	condition = [tripadvisor['SA']<0, tripadvisor['SA']==0, tripadvisor['SA']>0]
# 	choices = ['Negative','Neutral','Positive']
# 	tripadvisor['Sentiment']=np.select(condition,choices)

# 	###########################################
# 	filename = 'category_classification.ompad'
# 	def clean_text(text):
# 		text = text.lower()
# 		text = re.sub(r"what's", "what is ", text)
# 		text = re.sub(r"\'s", " ", text)
# 		text = re.sub(r"\'ve", " have ", text)
# 		text = re.sub(r"can't", "can not ", text)
# 		text = re.sub(r"n't", " not ", text)
# 		text = re.sub(r"i'm", "i am ", text)
# 		text = re.sub(r"\'re", " are ", text)
# 		text = re.sub(r"\'d", " would ", text)
# 		text = re.sub(r"\'ll", " will ", text)
# 		text = re.sub(r"\'scuse", " excuse ", text)
# 		text = re.sub('\W', ' ', text)
# 		text = re.sub('\s+', ' ', text)
# 		text = text.strip(' ')
# 		return text
    
# 	loaded_model = joblib.load(filename)
# 	classes = []
# 	prediction = loaded_model.predict(tripadvisor['comments'].apply(clean_text))

# 	for i in prediction:
# 		classes.append(i)

# 	categories = ['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']

# 	classification = pd.DataFrame(classes, columns = categories)	
# 	tripadvisor[['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']]=classification[['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']]

# 	tripadvisor.to_csv('%tripadvisor%_Result.csv', index=False)

# 	###########################################
# 	stop_words = stopwords.words('english')
# 	extension.append('hotel')
# 	extension.append('shangri_la')
# 	print(extension)
# 	stop_words.extend(extension)
# 	data=tripadvisor.comments.values.tolist()
# 	data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
# 	data = [re.sub('\s+', ' ', sent) for sent in data]
# 	data = [re.sub("\'", "", sent) for sent in data]
# 	# remove stock market tickers like $GE
# 	data = [re.sub(r'\$\w*', '', sent)for sent in data]
# 	# remove old style retext text "RT"
# 	data = [re.sub(r'^RT[\s]+', '', sent)for sent in data]
# 	# remove hyperlinks
# 	data = [re.sub(r'https?:\/\/.*[\r\n]*', '', sent)for sent in data]
# 	# remove hashtags symbols in a hashtagged word	
# 	# only removing the hash # sign from the word
# 	data = [re.sub(r'#', '', sent)for sent in data]
# 	# remove @users
# 	data = [re.sub(r'@[\w]*', '', sent)for sent in data]

# 	def sent_to_words(sentences):
# 		for sentence in sentences:
# 			yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

# 	data_words = list(sent_to_words(data))

# 	bigram = gensim.models.Phrases(data_words, min_count=5, threshold=5) # higher threshold fewer phrases. 

# 	bigram_mod = gensim.models.phrases.Phraser(bigram)

# 	def remove_stopwords(texts):
# 		return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

# 	def make_bigrams(texts):
# 		return [bigram_mod[doc] for doc in texts]

# 	def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
# 		"""https://spacy.io/api/annotation"""
# 		texts_out = []
# 		for sent in texts:
# 			doc = nlp(" ".join(sent)) 
# 			texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
# 		return texts_out

# 	data_words_nostops = remove_stopwords(data_words)


# 	data_words_bigrams = make_bigrams(data_words_nostops)


# 	# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# 	# python3 -m spacy download en
# 	nlp = spacy.load('en', disable=['parser', 'ner'])

# 	# Do lemmatization keeping only noun, adj, vb, adv
# 	data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN'])#''NOUN',ADJ', 'VERB', 'ADV'])

# 	id2word = Dictionary(data_lemmatized)

# 	texts = data_lemmatized

# 	corpus = [id2word.doc2bow(text) for text in texts]
	
# 	goodLdaModel = LdaModel(corpus=corpus, id2word=id2word, iterations=100000, num_topics=1)

# 	words = []
# 	for t in range(goodLdaModel.num_topics):
# 		print (goodLdaModel.show_topic(t))
# 		words.append([str(k) for k,v in goodLdaModel.show_topic(t)])
# 		#print('Printing for Topic ' + str(t)) 
# 		plt.figure()
# 		plt.imshow(WordCloud().generate(" ".join([str(k) for k,v in goodLdaModel.show_topic(t)])))
# 		plt.axis("off")
# 		plt.title("Topic #" + str(t))
# 		plt.savefig(str(t)+'.png', format = 'png', dpi=300)
# 		plt.close()
# 	words
# 	word = []
# 	words = remove_stopwords(words)
# 	for i in words:
# 		for j in i:
# 			word.append(j)
# 	semantic = []
# 	pos = []
# 	neu = []
# 	neg = []
# 	for i in word:
# 		semantic.append(i)
# 		positive = tripadvisor.loc[tripadvisor['SA']>0]
# 		pos.append(positive.comments.str.count(i).sum())
# 		neutral = tripadvisor.loc[tripadvisor['SA']==0]
# 		neu.append(neutral.comments.str.count(i).sum())
# 		negative = tripadvisor.loc[tripadvisor['SA']<0]
# 		neg.append(negative.comments.str.count(i).sum())

# 	semantic_mention = pd.DataFrame({'word':semantic,'Positive Mention':pos,'Neutral Mention':neu, 'Negative Mention':neg})
# 	#semantic_mention=semantic_mention.loc[(semantic_mention['Positive Mention']!=0)&(semantic_mention['Neutral Mention']!=0)&(semantic_mention['Negative Mention']!=0)]
# 	semantic_mention.to_csv('%trip_advisor%_semantic_mention.csv', index=False)

#######################################################

print('Analyzing Agoda')
for i in agoda:
	agoda = pd.read_csv(str(i))
	agoda = agoda.replace(np.nan, '', regex=True)
	agoda['comments']=agoda['comments'].dropna()

	agoda['SA'] = np.array([ analyze_sentiment(comments) for comments in agoda['comments'] ])

	pos_texts = int(len(agoda.loc[agoda.SA > 0]))
	neu_texts = int(len(agoda.loc[agoda.SA == 0]))
	neg_texts = int(len(agoda.loc[agoda.SA < 0]))

	print("Percentage of Positive Reviews: {}%".format(pos_texts*100/len(agoda['SA'])))
	print("Percentage of Neutral Reviews: {}%".format(neu_texts*100/len(agoda['SA'])))
	print("Percentage of Negative Reviews: {}%".format(neg_texts*100/len(agoda['SA'])))
	sentiment_count = pd.DataFrame({'%Positive':[pos_texts*100/len(agoda['SA'])],'%Neutral':[neu_texts*100/len(agoda['SA'])],'%Negative':[ neg_texts*100/len(agoda['SA'])]})
	print(sentiment_count.head(5))
	sentiment_count.to_csv('%agoda%_sentiment_count.csv',index=False)
	condition = [agoda['SA']<0, agoda['SA']==0, agoda['SA']>0]
	choices = ['Negative','Neutral','Positive']
	agoda['Sentiment']=np.select(condition,choices)
	###########################################

	def clean_text(text):
		text = text.lower()
		text = re.sub(r"what's", "what is ", text)
		text = re.sub(r"\'s", " ", text)
		text = re.sub(r"\'ve", " have ", text)
		text = re.sub(r"can't", "can not ", text)
		text = re.sub(r"n't", " not ", text)
		text = re.sub(r"i'm", "i am ", text)
		text = re.sub(r"\'re", " are ", text)
		text = re.sub(r"\'d", " would ", text)
		text = re.sub(r"\'ll", " will ", text)
		text = re.sub(r"\'scuse", " excuse ", text)
		text = re.sub('\W', ' ', text)
		text = re.sub('\s+', ' ', text)
		text = text.strip(' ')
		return text
   
	loaded_model = joblib.load(filename)
	classes = []
	prediction = loaded_model.predict(agoda['comments'].apply(clean_text))

	for i in prediction:
		classes.append(i)

	categories = ['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']

	classification = pd.DataFrame(classes, columns = categories)	
	agoda[['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']]=classification[['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']]
	agoda.to_csv('%agoda%_Result.csv', index=False)

	###########################################
	stop_words = stopwords.words('english')
	extension.append('hotel')
	extension.append('shangri_la')
	print(extension)
	stop_words.extend(extension)
	data=agoda.comments.values.tolist()
	data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
	data = [re.sub('\s+', ' ', sent) for sent in data]
	data = [re.sub("\'", "", sent) for sent in data]
	# remove stock market tickers like $GE
	data = [re.sub(r'\$\w*', '', sent)for sent in data]
	# remove old style retext text "RT"
	data = [re.sub(r'^RT[\s]+', '', sent)for sent in data]
	# remove hyperlinks
	data = [re.sub(r'https?:\/\/.*[\r\n]*', '', sent)for sent in data]
	# remove hashtags symbols in a hashtagged word	
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
	data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN'])#''NOUN',ADJ', 'VERB', 'ADV'])

	id2word = Dictionary(data_lemmatized)

	texts = data_lemmatized

	corpus = [id2word.doc2bow(text) for text in texts]
	
	goodLdaModel = LdaModel(corpus=corpus, id2word=id2word, iterations=100000, num_topics=1)

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
	words
	word = []
	words = remove_stopwords(words)
	for i in words:
		for j in i:
			word.append(j)
	semantic = []
	pos = []
	neu = []
	neg = []
	for i in word:
		semantic.append(i)
		positive = agoda.loc[agoda['SA']>0]
		pos.append(positive.comments.str.count(i).sum())
		neutral = agoda.loc[agoda['SA']==0]
		neu.append(neutral.comments.str.count(i).sum())
		negative = agoda.loc[agoda['SA']<0]
		neg.append(negative.comments.str.count(i).sum())

	semantic_mention = pd.DataFrame({'word':semantic,'Positive Mention':pos,'Neutral Mention':neu, 'Negative Mention':neg})
	#semantic_mention=semantic_mention.loc[(semantic_mention['Positive Mention']!=0)&(semantic_mention['Neutral Mention']!=0)&(semantic_mention['Negative Mention']!=0)]
	semantic_mention.to_csv('%agoda%_semantic_mention.csv', index=False)

#####################################
print('Analyzing Booking.com')
for i in booking:
	booking = pd.read_csv(str(i))
	booking = booking.replace(np.nan, '', regex=True)
	booking['comments']=booking['comments'].dropna()

	booking['SA'] = np.array([ analyze_sentiment(comments) for comments in booking['comments'] ])

	pos_texts = int(len(booking.loc[booking.SA > 0]))
	neu_texts = int(len(booking.loc[booking.SA == 0]))
	neg_texts = int(len(booking.loc[booking.SA < 0]))

	print("Percentage of Positive Reviews: {}%".format(pos_texts*100/len(booking['SA'])))
	print("Percentage of Neutral Reviews: {}%".format(neu_texts*100/len(booking['SA'])))
	print("Percentage of Negative Reviews: {}%".format(neg_texts*100/len(booking['SA'])))
	sentiment_count = pd.DataFrame({'%Positive':[pos_texts*100/len(booking['SA'])],'%Neutral':[neu_texts*100/len(booking['SA'])],'%Negative':[ neg_texts*100/len(booking['SA'])]})
	print(sentiment_count.head(5))
	sentiment_count.to_csv('%booking%_sentiment_count.csv',index=False)

	condition = [booking['SA']<0, booking['SA']==0, booking['SA']>0]
	choices = ['Negative','Neutral','Positive']
	booking['Sentiment']=np.select(condition,choices)
	###########################################

	def clean_text(text):
		text = text.lower()
		text = re.sub(r"what's", "what is ", text)
		text = re.sub(r"\'s", " ", text)
		text = re.sub(r"\'ve", " have ", text)
		text = re.sub(r"can't", "can not ", text)
		text = re.sub(r"n't", " not ", text)
		text = re.sub(r"i'm", "i am ", text)
		text = re.sub(r"\'re", " are ", text)
		text = re.sub(r"\'d", " would ", text)
		text = re.sub(r"\'ll", " will ", text)
		text = re.sub(r"\'scuse", " excuse ", text)
		text = re.sub('\W', ' ', text)
		text = re.sub('\s+', ' ', text)
		text = text.strip(' ')
		return text 
  
	loaded_model = joblib.load(filename)
	classes = []
	prediction = loaded_model.predict(booking['comments'].apply(clean_text))

	for i in prediction:
		classes.append(i)

	categories = ['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']

	classification = pd.DataFrame(classes, columns = categories)	
	booking[['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']]=classification[['Cleanliness', 'Comfort&Facilities', 'Food', 'Internet', 'Location', 'Staff', 'Value for money']]

	booking.to_csv('%booking%_Result.csv', index=False)
        #######################
	stop_words = stopwords.words('english')
	extension.append('hotel')
	extension.append('shangri_la')
	print(extension)
	stop_words.extend(extension)
	data=booking.comments.values.tolist()
	data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
	data = [re.sub('\s+', ' ', sent) for sent in data]
	data = [re.sub("\'", "", sent) for sent in data]
	# remove stock market tickers like $GE
	data = [re.sub(r'\$\w*', '', sent)for sent in data]
	# remove old style retext text "RT"
	data = [re.sub(r'^RT[\s]+', '', sent)for sent in data]
	# remove hyperlinks
	data = [re.sub(r'https?:\/\/.*[\r\n]*', '', sent)for sent in data]
	# remove hashtags symbols in a hashtagged word	
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
	data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN'])#''NOUN',ADJ', 'VERB', 'ADV'])

	id2word = Dictionary(data_lemmatized)

	texts = data_lemmatized

	corpus = [id2word.doc2bow(text) for text in texts]
	
	goodLdaModel = LdaModel(corpus=corpus, id2word=id2word, iterations=100000, num_topics=1)

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
	words
	word = []
	words = remove_stopwords(words)
	for i in words:
		for j in i:
			word.append(j)
	semantic = []
	pos = []
	neu = []
	neg = []
	for i in word:
		semantic.append(i)
		positive = booking.loc[booking['SA']>0]
		pos.append(positive.comments.str.count(i).sum())
		neutral = booking.loc[booking['SA']==0]
		neu.append(neutral.comments.str.count(i).sum())
		negative = booking.loc[booking['SA']<0]
		neg.append(negative.comments.str.count(i).sum())

	semantic_mention = pd.DataFrame({'word':semantic,'Positive Mention':pos,'Neutral Mention':neu, 'Negative Mention':neg})
	#semantic_mention = semantic_mention.loc[(semantic_mention['Positive Mention']!=0)&(semantic_mention['Neutral Mention']!=0)&(semantic_mention['Negative Mention']!=0)]
	semantic_mention.to_csv('%booking%_semantic_mention.csv', index=False)
