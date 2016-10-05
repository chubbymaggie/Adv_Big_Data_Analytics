from yahoo_finance import Share
import time
from sklearn import svm
import numpy
from sklearn.svm import SVR

import numpy as np
import matplotlib.pyplot as plt

import pylab as pl

import nltk
import string
import os

from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


token_dict = {}
keyword_dict = {}

factor = []

stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


list_company = []
list_company.append(['TSLA','tesla'])
list_company.append(['MCD','mcdonald'])
list_company.append(['IBM','ibm'])
list_company.append(['BAC','bank of america','boa'])
list_company.append(['C','citi','citigroup'])
list_company.append(['AAPL','apple'])
list_company.append(['NKE','nike'])
list_company.append(['TWTR','twitter'])
list_company.append(['GE','general electric'])
list_company.append(['T','at&t'])

all_history = []
all_predict = []
svm_fiterror = []

for i in range(10):
    svm_fiterror.append([])

corrections = []
for i in range(10):
    corrections.append([])




if __name__ == '__main__':
    
    for i in range(10):
        s = Share(list_company[i][0])
        s.refresh()
        x = s.get_historical('2016-02-25', '2016-03-10')
        if(i==3):
            del x[0]
        #print(len(x))
        
        l = []
        for j in range(len(x)):
            l.append((float(x[j]['High'])+float(x[j]['Low']))/2)
        all_history.append(l)



    print('finish collecting stock prices')
    


    for i in range(10):
        x=[[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
        xres = np.reshape(x, (-1, 1))
        y = all_history[i]
        clf = svm.SVR()
        clf.fit(xres, y)
        SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=1,\
            gamma='auto',kernel='rbf', max_iter=-1, shrinking=True, \
            tol=0.001, verbose=False)
            
        all_predict.append(clf.predict(np.reshape([11], (-1, 1)))[0])


#calculate error for the 4 most recent days: error = actual - svm-fitted


        svm_fiterror[i].append((y[6]-clf.predict(np.reshape([7], (-1, 1)))[0])/y[6]*100)
        svm_fiterror[i].append((y[7]-clf.predict(np.reshape([8], (-1, 1)))[0])/y[7]*100)
        svm_fiterror[i].append((y[8]-clf.predict(np.reshape([9], (-1, 1)))[0])/y[8]*100)
        svm_fiterror[i].append((y[9]-clf.predict(np.reshape([10], (-1, 1)))[0])/y[9]*100)


#        if i == 3:
#            xx=[]
#            yy=[]
#            k=0
#            while k<12:
#                k = k+0.1
#                xx.append(k)
#                yy.append(clf.predict(np.reshape([k], (-1, 1))))
#            plt.plot(xx, yy)
#            plt.plot(x,y,'o')
#            plt.show()

    print('finished svm fitting and calculated fitting errors for the latest 4 days')

#print(all_predict)


    for filen in range(4):
        for i in range(8):
            company = list_company[i][0]
            filenumber = str(filen+6)
            file_path = '/Users/yaoxiao/Desktop/Twitter_0'+filenumber+'/'+company+'.txt'
            shakes = open(file_path, 'r')
            text = shakes.read()
            lowers = text.lower()
            no_punctuation = lowers.translate(None, string.punctuation)
            tokens = nltk.word_tokenize(no_punctuation)
            filtered = [w for w in tokens if not w in stopwords.words('english')]
            stemmer = PorterStemmer()
            stemmed = stem_tokens(filtered, stemmer)
            count = Counter(stemmed)
            top10 = count.most_common(10)
            for w in top10:
                if(keyword_dict.has_key(w[0])):
                    keyword_dict[w[0]] = keyword_dict[w[0]] + svm_fiterror[i][filen]
                else:
                    keyword_dict[w[0]] = svm_fiterror[i][filen]

    print('finished building up keywords and their absolute influence in stock')


    for filen in range(4):
        for i in range(8):
            company = list_company[i][0]
            filenumber = str(filen+6)
            file_path = '/Users/yaoxiao/Desktop/Twitter_0'+filenumber+'/'+company+'.txt'
            shakes = open(file_path, 'r')
            text = shakes.read()
            lowers = text.lower()
            no_punctuation = lowers.translate(None, string.punctuation)
            tokens = nltk.word_tokenize(no_punctuation)
            filtered = [w for w in tokens if not w in stopwords.words('english')]
            stemmer = PorterStemmer()
            stemmed = stem_tokens(filtered, stemmer)
            count = Counter(stemmed)
            top10 = count.most_common(10)
            score = 0
            for w in top10:
                if(keyword_dict.has_key(w[0])):
                    score = score + keyword_dict[w[0]]
            if(score != 0):
                factor.append(svm_fiterror[i][filen]/score)


    print('finished calculating the factor')


    final_factor = sum(factor)/len(factor)


    for filen in range(4):
        for i in range(8):
            company = list_company[i][0]
            filenumber = str(filen+6)
            file_path = '/Users/yaoxiao/Desktop/Twitter_0'+filenumber+'/'+company+'.txt'
            shakes = open(file_path, 'r')
            text = shakes.read()
            lowers = text.lower()
            no_punctuation = lowers.translate(None, string.punctuation)
            tokens = nltk.word_tokenize(no_punctuation)
            filtered = [w for w in tokens if not w in stopwords.words('english')]
            stemmer = PorterStemmer()
            stemmed = stem_tokens(filtered, stemmer)
            count = Counter(stemmed)
            top10 = count.most_common(10)
            score = 0
            for w in top10:
                if(keyword_dict.has_key(w[0])):
                    score = score + keyword_dict[w[0]]
            errpercent = score * final_factor
            corrections[i].append((all_history[i][filen+6] - svm_fiterror[i][filen]/100*all_history[i][filen+6])*(1+errpercent/100))

            

    x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = all_history[3]
    plt.plot(x,y,'o',color='blue')

    for i in range(4):
        x = i+7
        y = all_history[3][i+6] - svm_fiterror[3][i]/100*all_history[3][i+6]
        plt.plot(x,y,'o',color='red')

    for i in range(4):
        x = i+7
        y = corrections[3][i]
        plt.plot(x,y,'o',color='green')


    plt.xlim(0,12)

    plt.show()


    print(final_factor)


    for i in range(8):
        company = list_company[i][0]
        filenumber = str(filen+6)
        file_path = '/Users/yaoxiao/Desktop/Twitter_Test/'+company+'.txt'
        shakes = open(file_path, 'r')
        text = shakes.read()
        lowers = text.lower()
        no_punctuation = lowers.translate(None, string.punctuation)
        tokens = nltk.word_tokenize(no_punctuation)
        filtered = [w for w in tokens if not w in stopwords.words('english')]
        stemmer = PorterStemmer()
        stemmed = stem_tokens(filtered, stemmer)
        count = Counter(stemmed)
        top10 = count.most_common(10)
        score = 0
        for w in top10:
            if(keyword_dict.has_key(w[0])):
                score = score + keyword_dict[w[0]]
        errpercent = score * final_factor
        all_predict[i]=all_predict[i]*(1+errpercent/100)

    print(all_predict)



















