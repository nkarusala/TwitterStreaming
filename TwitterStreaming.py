#!/usr/bin/env python

from textwrap import TextWrapper

import tweepy
import os


import json

if (os.path.exists(os.getcwd() + os.sep + "indiaTweets.json")):
    print "file exists, opening in append mode"
    file = open("indiaTweets.json", "a")
else:
    print "file doesn't exist, opening in write mode"
    file = open("indiaTweets.json", "w")

file.write("{")

counter = 0;

class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    #def __init__(self, keyword=[], user=[], location="", api=None):
        #super(StreamWatcherListener, self).__init__()
        #self.keyword = keyword[0]
        #self.user = user[0]
        #self.location = location

    def __init__(self, keywords=[], api=None):
        super(StreamWatcherListener, self).__init__()
        self.keywords = keywords

    def on_data(self, data):
        global counter;
        decoded = json.loads(data)

        try:
            if any(word in decoded['text'] for word in self.keywords):
                #print "useful data found from:"
                counter += 1;
                file.write('"' + "tweet" + str(counter) + '": ')
                print decoded['user']['screen_name']
                json.dump(decoded, file, indent=4, ensure_ascii=True)
                file.write(",")
                #print "is this happening1"
                file.write("\n")
                #print "is this happening2"
        except:
            #print "tried and except-ed"
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def main():


    # Prompt for login credentials and setup stream object
    consumer_key = "qRqv74RtDSHDLYduSlhjpOaPN"
    consumer_secret = "z3FQaAGaB6YTEL7OQr48MlnPk6RFJjaA3kW4mnZ7lehKsjcDPl"
    access_token = "2830438275-1dmOOhi3CLknDYL5MnvNytZyPQL46JZpDKQrdnv"
    access_token_secret = "qDHAYBJBlNtsw7NCGA62UJxcgK58pCKnxImsRsDWavwVt"

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Prompt for mode of streaming
    keywords = ["autism", "autistic", "developmental disorder", "child development", "centre for autism", "aspergers"]
    latUpper = 36
    latLow = 8
    lonLow = 70
    lonUpper = 88
    stream = tweepy.Stream(auth, StreamWatcherListener(keywords), timeout=None)
    stream.filter(locations=[lonLow,latLow,lonUpper,latUpper])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        #print '\nGoodbye!'
        if (os.stat("indiaTweets.json").st_size != 0):
            file.seek(-1, os.SEEK_END)
            file.truncate()
            file.seek(-1, os.SEEK_END)
            file.truncate()
            file.seek(-1, os.SEEK_END)
            file.truncate()
        file.write("}")
        file.close()