# -*- coding: utf-8 -*-
"""
Katie Gangeline, Matthew Miller

- lemmatization script
"""

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

def Lem(files,newfile):
    fw = open('lemmatized.txt', 'w')
    #ret_text=""
    for file in files:
        f=open(file)
        for line in f:
            article,label=line.strip().split('\t')
            article=re.sub('[^0-9A-Za-z]',' ',article).strip()
            try:
                #ret_text+= lemmatize(article) + '\t' + label + '\n'
                fw.write(lemmatize(article) + '\t' + label + '\n')
            except:
                continue
        f.close()
    #fw.write(ret_text)
    fw.close()
    return

if __name__=='__main__':    
    files={'train_Fox_pol.txt','Liberal_articles.txt'}
    #articles,labels=loadData(files)
    articles,labels=Lem(files)
