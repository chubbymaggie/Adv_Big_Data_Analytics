from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import nltk
import re



access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


list_company = []
list_company.append(['GE','general electric'])
list_company.append(['TSLA','tesla'])
list_company.append(['MCD','mcdonald'])
list_company.append(['IBM','ibm'])
list_company.append(['BAC','bank of america','boa'])
list_company.append(['C','citi','citigroup'])
list_company.append(['AAPL','apple'])
list_company.append(['NKE','nike'])
list_company.append(['TWTR','twitter'])
list_company.append(['T','at&t'])


alllist = ['General Electric','Tesla','tesla','McDonald','mcdonald'\
           'ibm','IBM','bank of america','boa','citi','citigroup'\
           'apple','Apple','at&t','att','Nike','nike','Twitter','twitter']


class StdOutListener(StreamListener):
    
    def on_data(self, data):
        
        try:
            tweet = json.loads(data)
            s = tweet.get('text', None).lower()
            s = s + ' '
            s = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', s)
            
            cur_i = 0
            for i in range(10):
                find = 0
                keywords = list_company[i]
                for j in range(len(keywords)-1):
                    if(s.find(keywords[j+1]) != -1):
                        find = 1
                        cur_i = i
                        print list_company[i][0]
                        break
                if(find == 1):
                    break
        
            if(find == 0):
                return True
            company_name = list_company[cur_i][0]
            fname = '/Users/yaoxiao/Desktop/Twitter_Test/' + company_name + '.txt'
            f = open(fname,'a')
            f.write(s)
            f.close()
    
        except:
            return True
        
        return True
    
    def on_error(self, status):
        print status


if __name__ == '__main__':
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    
    stream.filter(languages=['en'],track=alllist)






















