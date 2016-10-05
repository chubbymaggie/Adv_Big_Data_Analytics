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
import math
import nltk


if __name__ == "__main__":
    
    sc = SparkContext()
    file = sc.textFile(sys.argv[1],1)
    microsoft_rdd = sc.parallelize(file.filter(lambda line: "microsoft" in line.lower()).map(lambda s: re.findall("\d+[\.]?\d*", s)).first())
    google_rdd = sc.parallelize(file.filter(lambda line: "google" in line.lower()).map(lambda s: re.findall("\d+[\.]?\d*", s)).first())
    ibm_rdd = sc.parallelize(file.filter(lambda line: "ibm" in line.lower()).map(lambda s: re.findall("\d+[\.]?\d*", s)).first())
    oracle_rdd = sc.parallelize(file.filter(lambda line: "oracle" in line.lower()).map(lambda s: re.findall("\d+[\.]?\d*", s)).first())
    yahoo_rdd = sc.parallelize(file.filter(lambda line: "yahoo" in line.lower()).map(lambda s: re.findall("\d+[\.]?\d*", s)).first())
    
    all_rdds = [microsoft_rdd, google_rdd, ibm_rdd, oracle_rdd, yahoo_rdd]
    
    
    for x in all_rdds:
        numerics = x.map(lambda string: float(string))
        stats = numerics.stats()
        stddev = stats.stdev()
        mean = stats.mean()
        reasonable = numerics.filter(lambda a: math.fabs(a-mean) < 3*stddev)
        print reasonable.collect()

    sc.stop()









