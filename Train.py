from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
import requests
from operator import itemgetter
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score


def loadData(files):
    articles=[]
    labels=[]
    for file in files:
        f=open(file)
        for line in f:
            article,label=line.strip().split('\t')
            articles.append(article.lower())
            labels.append(label)
        f.close()
    return articles,labels
    
    
if __name__=='__main__':

    files={'train_Fox_pol.txt','Liberal_articles.txt'}
    articles,labels=loadData(files)
    articles_train, articles_test, labels_train, labels_test = train_test_split(articles, labels, test_size=0.25)


    counter = CountVectorizer(stop_words='english')
    counter.fit_transform(articles_train)
    counts_train=counter.transform(articles_train)
    counts_test=counter.transform(articles_test)
    
    #train classifier
    clf = MultinomialNB()
    
    #train all classifier on the same datasets
    clf.fit(counts_train,labels_train)
    
    #use hard voting to predict (majority voting)
    pred=clf.predict(counts_test)
    
    #print accuracy
    print (accuracy_score(pred,labels_test))
    
    
    #print(counts_train)
