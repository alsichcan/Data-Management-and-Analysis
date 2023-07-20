from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import numpy as np
import pickle
import os

np.random.seed(0)

categories = ['opinion', 'business', 'world', 'us', 'arts', 'sports', 'books', 'movies']

train_data = load_files(container_path='text/train', categories=categories, shuffle=True,
                        encoding='utf-8', decode_error='replace')

# TODO - 2-1-1. Build pipeline for Naive Bayes Classifier
clf_nb = Pipeline([('vect', CountVectorizer(stop_words='english', analyzer='word', min_df=5, max_df=0.5)),
                    ('tfidf', TfidfTransformer()),
                    ('clf', MultinomialNB(alpha=0.5))])
clf_nb.fit(train_data.data, train_data.target)

# TODO - 2-1-2. Build pipeline for SVM Classifier
clf_svm = Pipeline([('vect', CountVectorizer(stop_words='english', analyzer='word', ngram_range=(1,4), min_df=5, max_df=0.5)),
                   ('tfidf', TfidfTransformer()),
                   ('clf', SVC(kernel='linear', C=0.7))])
clf_svm.fit(train_data.data, train_data.target)

test_data = load_files(container_path='text/test', categories=categories, shuffle=True,
                        encoding='utf-8', decode_error='replace')
docs_test = test_data.data

predicted = clf_nb.predict(docs_test)
print("NB accuracy : %d / %d" % (np.sum(predicted==test_data.target), len(test_data.target)))
print(metrics.classification_report(test_data.target, predicted, target_names=test_data.target_names))
print(metrics.confusion_matrix(test_data.target, predicted))

predicted = clf_svm.predict(docs_test)
print("SVM accuracy : %d / %d" % (np.sum(predicted==test_data.target), len(test_data.target)))
print(metrics.classification_report(test_data.target, predicted, target_names=test_data.target_names))
print(metrics.confusion_matrix(test_data.target, predicted))

TEAM = 2

with open('DMA_project3_team%02d_nb.pkl' % TEAM, 'wb') as f1:
    pickle.dump(clf_nb, f1)

with open('DMA_project3_team%02d_svm.pkl' % TEAM, 'wb') as f2:
    pickle.dump(clf_svm, f2)
