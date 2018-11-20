from sklearn.model_selection import train_test_split

def loadData(files):
    articles=[]
    labels=[]
    for file in files:
        f=open(file1)
        for line in f:
            article,label=line.strip().split('\t')
            articles.append(article.lower())
            labels.append(label)
        f.close()
    return articles,labels
    
    
if __name__=='__main__':
    file1='Liberal_articles.txt'
    file2='train_Fox.txt'
    files={'Liberal_articles.txt','train_Fox.txt'}
    articles,labels=loadData(files)
    articles_train, articles_test, labels_train, labels_test = train_test_split(articles, labels, test_size=0.25)


    counter = CountVectorizer(stop_words=None)
    counts_train=counter.fit_transform(articles_train)
    counts_test=counter.fit_transform(articles_test)
    
    
    
    #print(counts_train)
