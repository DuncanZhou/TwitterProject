#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import numpy as np
'''
load data
'''
twenty_train = datasets.load_files("/home/duncan/data/20news-bydate/20news-bydate-train")
twenty_test = datasets.load_files("/home/duncan/data/20news-bydate/20news-bydate-test")

print len(twenty_train.target_names),len(twenty_train.data),len(twenty_test.target_names),len(twenty_test.data)

print twenty_train.target[:10]
# count word frequency
count_vect = CountVectorizer(stop_words="english", decode_error = "ignore")
X_train_counts = count_vect.fit_transform(twenty_train.data)
print X_train_counts.shape

#TF-IDF features extract
tf_transformer = TfidfTransformer(use_idf = False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
print X_train_tf.shape

#classifier is training
clf = MultinomialNB().fit(X_train_tf,twenty_train.target)

clf2 = SGDClassifier(loss='hinge',penalty = 'l2',alpha = 1e-3,random_state=42).fit(X_train_tf,twenty_train.target)

#predict the new documents
docs_news = ['God is love','OpenGL on the GPU is fast']
X_new_counts = count_vect.transform(docs_news)
X_new_tfidf = tf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

print "###########Bayes Classifier#############"
for doc,category in zip(docs_news,predicted):
    print("%r => %s") % (doc,twenty_train.target_names[category])

predicted2 = clf2.predict(X_new_tfidf)

print "###########SGD Classifier#############"
for doc,category in zip(docs_news,predicted2):
    print("%r => %s") % (doc,twenty_train.target_names[category])

# evaluate the classifier
print "###########Bayes Classifier#############"
text_clf = Pipeline([('vect',CountVectorizer(stop_words="english",decode_error='ignore')),('tfidf',TfidfTransformer()),('clf',MultinomialNB()),])
text_clf = text_clf.fit(twenty_train.data,twenty_train.target)

print "model has been writen into the disk"
joblib.dump(text_clf,'/home/duncan/sklearn-bayesclf-doc')

docs_test = twenty_test.data
predicted = text_clf.predict(docs_test)
print np.mean(predicted == twenty_test.target)

print "###########SGD Classifier#############"
text_clf_2 = Pipeline([('vect',CountVectorizer(stop_words='english',decode_error='ignore')),
                       ('tfidf',TfidfTransformer()),
                       ('clf',SGDClassifier(loss = 'hinge',penalty = 'l2',
                                            alpha = 1e-3,n_iter = 5, random_state = 42)),
                       ])

text_clf_2 = text_clf_2.fit(twenty_train.data,twenty_train.target)

print "model has been writen into the disk"
joblib.dump(text_clf_2,'/home/duncan/sklearn-SGDclf-doc')

predicted = text_clf_2.predict(docs_test)

print np.mean(predicted == twenty_test.target)
