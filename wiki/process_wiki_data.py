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
    rdd = sc.textFile(sys.argv[1],1)
    rdd = rdd.map(lambda line: nltk.word_tokenize(line))
    tf = HashingTF()
    tfVectors = tf.transform(rdd).cache()
    idf = IDF()
    idfModel = idf.fit(tfVectors)
    tfIdfVectors = idfModel.transform(tfVectors)
    result = tfIdfVectors.collect()
    
    for x in result:
        print x

    sc.stop()









