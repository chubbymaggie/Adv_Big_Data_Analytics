import json
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from operator import add
from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.sql import HiveContext, Row

import nltk


if __name__ == "__main__":
    
    sc = SparkContext()
    file = sc.textFile(sys.argv[1],1)
    microsoft_rdd = file.filter(lambda line: "microsoft" in line.lower())
    google_rdd = file.filter(lambda line: "google" in line.lower())
    ibm_rdd = file.filter(lambda line: "ibm" in line.lower())
    oracle_rdd = file.filter(lambda line: "oracle" in line.lower())
    yahoo_rdd = file.filter(lambda line: "yahoo" in line.lower())
    
    def file_map(x):
        try:
            tweet = json.loads(x)
            
            if tweet.get('lang', None) != "en":
                return " "
            s = tweet.get('text', None)
            return " " + s.lower() + " "
        except:
            return " "

    def file_reduce(a,b):
        return a + b

    microsoft_after_map = microsoft_rdd.map(lambda s: file_map(s))
    microsoft_after_reduce = microsoft_after_map.reduce(lambda a, b: file_reduce(a,b))

    google_after_map = google_rdd.map(lambda s: file_map(s))
    google_after_reduce = google_after_map.reduce(lambda a, b: file_reduce(a,b))

    ibm_after_map = ibm_rdd.map(lambda s: file_map(s))
    ibm_after_reduce = ibm_after_map.reduce(lambda a, b: file_reduce(a,b))
    
    oracle_after_map = oracle_rdd.map(lambda s: file_map(s))
    oracle_after_reduce = oracle_after_map.reduce(lambda a, b: file_reduce(a,b))
    
    yahoo_after_map = yahoo_rdd.map(lambda s: file_map(s))
    yahoo_after_reduce = yahoo_after_map.reduce(lambda a, b: file_reduce(a,b))
    
    rdd = sc.parallelize([microsoft_after_reduce, google_after_reduce, ibm_after_reduce, oracle_after_reduce, yahoo_after_reduce]).map(lambda line: nltk.word_tokenize(line))
    tf = HashingTF()
    tfVectors = tf.transform(rdd).cache()


    idf = IDF()
    idfModel = idf.fit(tfVectors)
    tfIdfVectors = idfModel.transform(tfVectors)
    
    result = tfIdfVectors.collect()
    
    for x in result:
        print x


    sc.stop()









