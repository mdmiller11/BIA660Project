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
    
if __name__=='__main__':    
    files={'train_Fox_pol.txt','Liberal_articles.txt'}
    #files={'lemmatized.txt'}
    articles,labels=loadData(files)
    articles_train, articles_test, labels_train, labels_test = train_test_split(articles, labels, test_size=0.25)
    

    counter = CountVectorizer(stop_words='english',ngram_range=(1,2))
    counter.fit_transform(articles_train)
    counts_train=counter.transform(articles_train)
    counts_test=counter.transform(articles_test)
    
    #train classifier NB
    print("NB")
    clf = MultinomialNB()
    clf_fitted = classify(clf,counts_train, labels_train, counts_test,labels_test,grid=None)
        
    #DTREE
    print("DTree")
    clf2 = tree.DecisionTreeClassifier(max_depth = 8,criterion='gini',splitter='best')
    clf2_fitted = classify(clf2,counts_train, labels_train, counts_test,labels_test,grid=None)

    
    #DT_grid = [{'max_depth': [3,4,5,6,7,8,9,10,11,12],
    #            'criterion':['gini','entropy'],
     #           'splitter':['best','random']}]
    
    #gsclf2_fitted = classify(clf2,counts_train, labels_train, counts_test,labels_test,grid=DT_grid)



    #SVM
    print("SVM")
    clf3 = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape='ovr', degree=3, gamma='auto', kernel='linear',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
    
    clf3_fitted = classify(clf3,counts_train, labels_train, counts_test,labels_test,grid=None)
    
#==============================================================================
#     svm_grid=[{'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
#               'degree': [3,5]
#                }]

#==============================================================================
    

    #RF
    print("RF")
    clf4=RandomForestClassifier(n_estimators=500, max_depth=20, random_state=0,criterion='gini')
    
    clf4_fitted = classify(clf4,counts_train, labels_train, counts_test,labels_test,grid=None)
        
#==============================================================================
#     RF_grid=[{'n_estimators': [100,500,1000],
#               'max_depth': [10,20],
#                }]
# 
#==============================================================================
    # Boosting
    print("ADA Boosting RF")
    clf_Ada=AdaBoostClassifier(base_estimator=clf4, n_estimators=50, learning_rate=1.0)
    clfADA_fitted = classify(clf_Ada,counts_train, labels_train, counts_test,labels_test,grid=None)

#==============================================================================
#     #ANN
#     print("ANN")
#     clfANN = MLPClassifier(activation='relu', alpha=1e-05, batch_size='auto',
#               beta_1=0.95, beta_2=0.9995, early_stopping=False,
#               epsilon=1e-08, hidden_layer_sizes=(100,10,10),
#               learning_rate='constant', learning_rate_init=0.015,
#               max_iter=3000, momentum=0.9,
#               nesterovs_momentum=True, power_t=0.5, random_state=9,
#               shuffle=True, solver='adam', tol=0.00001,
#               validation_fraction=0.1, verbose=False, warm_start=False)
#     
#     clfANN_fitted = classify(clfANN,counts_train, labels_train, counts_test,labels_test,grid=None)
# 
#==============================================================================
    
#==============================================================================
#     ANN_grid=[{'learning_rate':['constant', 'invscaling', 'adaptive'],
#                'learning_rate_init':[.01,.015,.02]
#                }]
#     GSclfANN_fitted = classify(clfANN,counts_train, labels_train, counts_test,labels_test,grid=ANN_grid)
# 
#==============================================================================
    #predictors=[('NB',clf_fitted),('DTree',clf2_fitted),('SVM',clf3_fitted),('RF',clf4_fitted),('ADA',clfADA_fitted),('ANN',clfANN_fitted)]
    predictors=[('NB',clf_fitted),('DTree',clf2_fitted),('SVM',clf3_fitted),('RF',clf4_fitted),('ADA',clfADA_fitted),]
    print("Voting")
    VT=VotingClassifier(predictors)
    VT.fit(counts_train,labels_train)
    predVT=VT.predict(counts_test)
    print("VT")
    print (accuracy_score(predVT,labels_test))

    newfile='theblaze.txt'
    f=open(newfile,'r')
    c=f.read()
    c=re.sub('[^0-9A-Za-z]',' ',c).strip()
    c=c.replace('\n',' ')
    #c=lemmatize(c)
    c=c.lower()
    clist=[]
    clist.append(c)
    ctest=counter.transform(clist)
    print(clf_fitted.predict(ctest))
    print(clf2_fitted.predict(ctest))
    print(clf3_fitted.predict(ctest))
    print(clf4_fitted.predict(ctest))
    print(clfADA_fitted.predict(ctest))
    #print(clfANN_fitted.predict(ctest))
    print(VT.predict(ctest))

    
    newfile='newrepublic.txt'
    f=open(newfile,'r')
    d=f.read()
    d=re.sub('[^0-9A-Za-z]',' ',d).strip()
    d=d.replace('\n',' ')
    #d=lemmatize(d)
    d=d.lower()
    dlist=[]
    dlist.append(d)
    dtest=counter.transform(dlist)
    print(clf_fitted.predict(dtest))
    print(clf2_fitted.predict(dtest))
    print(clf3_fitted.predict(dtest))
    print(clf4_fitted.predict(dtest))
    print(clfADA_fitted.predict(dtest))
    #print(clfANN_fitted.predict(dtest))
    print(VT.predict(dtest))    
    
    newfile='washingtontimes.txt'
    f=open(newfile,'r',encoding='utf8',errors='ignore')
    c2=f.read()
    c2=re.sub('[^0-9A-Za-z]',' ',c2).strip()
    c2=c2.replace('\n',' ')
    c2=c2.lower()
    c2list=[]
    c2list.append(c2)
    c2test=counter.transform(c2list)
    print(clf_fitted.predict(c2test))
    print(clf2_fitted.predict(c2test))
    print(clf3_fitted.predict(c2test))
    print(clf4_fitted.predict(c2test))
    print(clfADA_fitted.predict(c2test))
    #print(clfANN_fitted.predict(c2test))
    print(VT.predict(c2test))     
    
    newfile='msnbc.txt'
    f=open(newfile,'r',encoding='utf8',errors='ignore')
    d2=f.read()
    d2=re.sub('[^0-9A-Za-z]',' ',d2).strip()
    d2=d2.replace('\n',' ')
    d2=d2.lower()
    d2list=[]
    d2list.append(d2)
    d2test=counter.transform(d2list)
    print(clf_fitted.predict(d2test))
    print(clf2_fitted.predict(d2test))
    print(clf3_fitted.predict(d2test))
    print(clf4_fitted.predict(d2test))
    print(clfADA_fitted.predict(d2test))
    #print(clfANN_fitted.predict(dtest))
    print(VT.predict(d2test)) 
    
    
