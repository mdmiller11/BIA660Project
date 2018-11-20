from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
import requests
from operator import itemgetter


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
    file1='Liberal_articles.txt'
    file2='train_Fox.txt'
    files={'train_Fox.txt','Liberal_articles.txt'}
    articles,labels=loadData(files)
    articles_train, articles_test, labels_train, labels_test = train_test_split(articles, labels, test_size=0.25)


    counter = CountVectorizer(stop_words=None)
    counts_train=counter.fit_transform(articles_train)
    counts_test=counter.fit_transform(articles_test)
    print(labels_train)
    
    
    #print(counts_train)
