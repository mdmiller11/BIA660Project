from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import VotingClassifier
from nltk.stem import WordNetLemmatizer
#import nltk
from nltk import load
import re
import numpy as np
from sklearn.feature_extraction import text 


def lemmatize(article):    
    _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
    tagger = load(_POS_TAGGER)
    wnpos = lambda e: ('a' if e[0].lower() == 'j' else e[0].lower()) if e[0].lower() in ['n', 'r', 'v'] else 'n'
    lemmatizer = WordNetLemmatizer()

    words=article.split(' ')
    tagged=tagger.tag(words)
    words2 = [lemmatizer.lemmatize(t[0],wnpos(t[1])) for t in tagged]
    ret=""
    for i in words2:
        ret += i + ' '
    return ret

def loadData(files):
    articles=[]
    labels=[]
    for file in files:
        f=open(file)
        for line in f:
            article,label=line.strip().split('\t')
            article=re.sub('[^0-9A-Za-z]',' ',article).strip()
            articles.append(article.lower())
            labels.append(label)
        f.close()
    return articles,labels

def classify(clf, counts_train, labels_train, counts_test,labels_test,grid=None):
    if(grid!=None):
        gsclf=GridSearchCV(clf, grid, cv=5)
        gsclf.fit(counts_train,labels_train)
        pred=gsclf.predict(counts_test)
        print(accuracy_score(pred,labels_test))
        print(gsclf.best_params_)
        return gsclf
    else:
        clf.fit(counts_train,labels_train)
        pred=clf.predict(counts_test)
        print(accuracy_score(pred,labels_test))
        return clf
    
def getKey(item):
    return item[0]

if __name__=='__main__':    
    #files={'train_Fox_pol.txt','Liberal_articles.txt'}
    files={'lemmatized.txt'}
    articles,labels=loadData(files)
    articles_train, articles_test, labels_train, labels_test = train_test_split(articles, labels, test_size=0.25)
    stopwordsextra=["fox","fox news"]
    stop_words = text.ENGLISH_STOP_WORDS.union(stopwordsextra)


    counter = CountVectorizer(stop_words=stop_words,ngram_range=(1,2))
    counter.fit_transform(articles_train)
    counts_train=counter.transform(articles_train)
    counts_test=counter.transform(articles_test)
    
    print("RF")
    clf4=RandomForestClassifier(n_estimators=500, max_depth=20, random_state=0,criterion='gini')
    
    clf4_fitted = classify(clf4,counts_train, labels_train, counts_test,labels_test,grid=None)
    x=clf4_fitted.feature_importances_
    y=np.array(counter.get_feature_names())
    z=[]
    for i in range(len(x)):
        z.append((x[i],y[i]))
    s=sorted(z,key=getKey, reverse=True)
    print(s[:20])

