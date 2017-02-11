#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import  StreamListener

ckey = "1PuhS8rjfnsx1ypPRuG190mOE"
csecret = "ov8v1UTcqTcNzHxYZglIWy95ExBPElSUzczZ3KhxXcONEHqjqw"
atoken = "819902790923390976-nLUVtg7ih9RUaBb9qp71rW85cVmSqRF"
asecret = "tkcwaZ7QMFfDtmnROlvCyUIW63t739RvPkql9EQZ3vQYN"

class listener(StreamListener):
    def on_data(self,data):
        print data
        return True

    def on_error(self, status_code):
        print status_code

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream = Stream(auth,listener())
twitterStream.filter(track=['car'])
