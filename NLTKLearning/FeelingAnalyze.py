#!/usr/bin/python
#-*-coding=utf-8-*-

import pickle
import numpy
import nltk
#分词
from nltk.tokenize import sent_tokenize,word_tokenize
#去除停词
from nltk.corpus import stopwords
#提取词干
from nltk.stem import PorterStemmer
# 引入语料
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
# lemmatize词形还原
from nltk.stem import WordNetLemmatizer
# 语料库样例
from nltk.corpus import gutenberg
# 引入wordnet词典
from nltk.corpus import wordnet
# 文本分类(影评二元分类)
import random
from nltk.corpus import movie_reviews
from nltk import FreqDist
# 使用scikitlearn框架
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
# 多学习器(投票分类)
from sklearn.linear_model import LogisticRegression,SGDClassifier
from nltk.classify import ClassifierI
# mode来选择最多的那个投票
from statistics import mode

ps = PorterStemmer()
'''Test the stemmer'''
example_words = ['python','pythoner','pythoning','pythoned','pythonly']
# for w in example_words:
# 	print(ps.stem(w))
# get the stop words
stop_words = set(stopwords.words('english'))

example_texts = "It is important to by very pythonly while you are pythoning with python. All pythoners have pythoned at least once."
words = word_tokenize(example_texts)
results = [w for w in words if not w in stop_words]
for w in results:
	print(ps.stem(w))

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

#train the punkt tokenizer
custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(sample_text)
lemmatizer = WordNetLemmatizer()
# 默认名词形式
print(lemmatizer.lemmatize("cacti"))
print(lemmatizer.lemmatize("cats"))
print(lemmatizer.lemmatize("better",pos="a"))

def process_tokenize_content(tokenized):
	try:
		for i in tokenized[:5]:
			words = nltk.word_tokenize(i)
			tagged = nltk.pos_tag(words)
			# 正则表达式表示分块规则
			chunkGram = r"""Chunk:{<RB.?>*<VB.?>*<NNP>+<NN>?}"""
			chunkParser = nltk.RegexpParser(chunkGram)
			# 文本分块
			chunked = chunkParser.parse(tagged)
			# chunked.draw()
			# print tagged
			# 实体识别
			namedEnt = nltk.ne_chunk(tagged,binary=True)
			#namedEnt.draw()
			#print namedEnt
			#print chunked
			# for subtree in chunked.subtrees(filter = lambda t:t.label()== 'Chunk'):
			# 	print subtree
	except Exception as e:
		print "something is wrong"
		print(str(e))
# 语料库样例
print "语料库样例:"
sample = gutenberg.raw("bible-kjv.txt")
tok = sent_tokenize(sample)
for x in range(5):
	print tok[x]
process_tokenize_content(tokenized)

# wordnet test
# synset同义词
print ("输出program的同义词")
syns = wordnet.synsets("program")
for i in syns:
	print(i.name())

print ("输出一个单词的同义词和反义词:")
synonyms = []
antonyms = []
for syn in wordnet.synsets("good"):
	# lemmas 是同义词
	for l in syn.lemmas():
		synonyms.append(l.name())
		# antonyms 是反义词
		if l.antonyms():
			antonyms.append(l.antonyms()[0].name())
print "good的同义词:	"
print (set(synonyms))
print "good的反义词:	"
print (set(antonyms))

# 词之间的相似性
w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')
print (w1.wup_similarity(w2))

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('car.n.01')
print (w1.wup_similarity(w2))

# 影评分类
print ("影评分类：")
documents = [(list(movie_reviews.words(fileid)),category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)
print(documents[1])

all_words = []
for w in movie_reviews.words():
	# 该小写
	all_words.append(w.lower())
# 词频统计
all_words = FreqDist(all_words)
print("输出词频出现前10的单词:")
print(all_words.most_common(10))

# 特征提取
# 选取前词频前3000个单词作为特征值
word_features = list(all_words.keys())[:3000]
#print word_features

# 将单词转化为特征
def find_features(document):
	words = set(document)
	features = {}
	for w in word_features:
		features[w] = (w in words)
	return features
print(find_features(movie_reviews.words('neg/cv000_29416.txt')))
featuresets = [(find_features(rev),category) for (rev,category) in documents]
training_set = featuresets[:1900]
testing_set = featuresets[1900:]
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier,testing_set)) * 100)
# 前15个对分类最有价值的特征单词
classifier.show_most_informative_features(15)
#保存训练好的模型
'''
save_classifiere = open("naivebayes.pickle","wb")
pickle.dump(classifier,save_classifier)
save_classifier.close()
'''
# 装载存储的模型
'''
classifier_f = open("naivebayes.pickle","rb")
classifier = pickle.load(classifier_f)
classifier_f.close()
'''
# 尝试scikitlearn框架的学习器
print("scikitlearn的MultinomialNB分类器")
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MultionmialNB accuracy percent:",nltk.classify.accuracy(MNB_classifier,testing_set) * 100)

# 多学习器
class VoteClassifier(ClassifierI):
	# 形参前有*，表示参数不止一个
	def __init__(self,*classifiers):
		self._classifiers = classifiers

	def classify(self,features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		return mode(votes)

	#计算置信度
	def confidence(self,features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)

		choice_votes = votes.count(mode(votes))
		conf = 1.0 * choice_votes / len(votes)
		return conf
SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
voted_classifier = VoteClassifier(classifier,SGDClassifier_classifier,LogisticRegression_classifier)
print("voted_classifier accuracy percent:",(nltk.classify.accuracy(voted_classifier,testing_set))*100)
#print("Classification:",voted_classifier.classify(testing_set[4][0]),"Confidence:",voted_classifier.confidence(testing_set[4][0])*100)









