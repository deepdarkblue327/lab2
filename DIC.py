# coding: utf-8

# In[35]:

import sys, jsonpickle, os, tweepy, json, urllib, urllib2, datetime, time, csv, re
import pandas as pd
from urllib2 import HTTPError
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import requests
import requests.packages.urllib3
from datetime import datetime, timedelta

today = datetime.now().strftime('%Y%m%d')
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
last_week = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')

requests.packages.urllib3.disable_warnings()
KEYWORD = sys.argv[1]


# In[36]:

API_KEY = "vlAsYUTr0d3dh1GDpF9WVkHBr"
API_SECRET = "LWkfBPJIYfdjOmJI6gmWvz94aw2W0CkQfaQcOeZUhL4Rntwvic"
# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)


searchQuery = "#" + KEYWORD
maxTweets = 45000
tweetsPerQry = 100
fName = "tweets.txt"
sinceId = yesterday if sys.argv[2] == "day" else last_week
max_id = -1L

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,max_id=str(max_id - 1),since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))


# In[37]:

my_demo_list = []
with open('tweets.txt','r') as json_file:
    jason = json_file.readline()
    all_data = []
    while jason != "":
        try:
            all_data.append(json.loads(jason))
            jason = json_file.readline()
        except:
            jason = json_file.readline()


# In[38]:

for each_dictionary in all_data:
    tweet_id = each_dictionary['id']
    whole_tweet = each_dictionary['text']
    only_url = whole_tweet[whole_tweet.find('https'):]
    favorite_count = each_dictionary['favorite_count']
    retweet_count = each_dictionary['retweet_count']
    created_at = each_dictionary['created_at']
    whole_source = each_dictionary['source']
    only_device = whole_source[whole_source.find('rel="nofollow">') + 15:-4]
    source = only_device
    retweeted_status = each_dictionary['retweeted_status'] = each_dictionary.get('retweeted_status', 'Original tweet')
    if retweeted_status == 'Original tweet':
        url = only_url
    else:
        retweeted_status = 'This is a retweet'
        url = 'This is a retweet'

    my_demo_list.append({'tweet_id': str(tweet_id),
                         'favorite_count': int(favorite_count),
                         'retweet_count': int(retweet_count),
                         'url': url,
                         'created_at': created_at,
                         'source': source,
                         'retweeted_status': retweeted_status,
                         'text': re.sub(r'[^\x00-\x7f]',r' ', whole_tweet),
                        })
tweet_json = pd.DataFrame(my_demo_list, columns = my_demo_list[0].keys())

tweets_text = list(tweet_json["text"])
with open("tweets_text_data.txt","w") as f:
    f.writelines(tweets_text)

tweet_json.to_csv("Tweets.csv", encoding='utf-8')


# In[40]:

# helper function to get json into a form I can work with
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


# In[41]:

# helpful function to figure out what to name individual JSON files        
def getJsonFileName(date, page, json_file_path):
    json_file_name = ".".join([date,str(page),'json'])
    json_file_name = "".join([json_file_path,json_file_name])
    return json_file_name


# In[42]:

# helpful function for processing keywords, mostly
def getMultiples(items, key):
    values_list = ""
    if len(items) > 0:
        num_keys = 0
        for item in items:
            if num_keys == 0:
                values_list = item[key]
            else:
                values_list =  "; ".join([values_list,item[key]])
            num_keys += 1
    return values_list


# In[43]:

# get the articles from the NYTimes Article API    
def getArticles(start_date, end_date, query, api_key, json_file_path):
    # LOOP THROUGH THE 101 PAGES NYTIMES ALLOWS FOR THAT DATE
    for page in range(101):
        print(page)
        time.sleep(3)
        for n in range(5):
            try:
                request_string = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + str(query) + "&begin_date=" + start_date + "&end_date=" + end_date + "&page=" + str(page) + "&api-key=" + api_key
                response = urllib2.urlopen(request_string)
                content = response.read()
                if content:
                    articles = convert(json.loads(content))
                    if len(articles["response"]["docs"]) >= 1:
                        json_file_name = getJsonFileName(start_date, page, json_file_path)
                        json_file = open(json_file_name, 'w')
                        json_file.write(content)
                        json_file.close()
                    else:
                        return
                time.sleep(3)
            except HTTPError as e:
                if e.code == 403:
                    print "Script hit a snag and got an HTTPError 403. Check your log file for more info."
                    return
                if e.code == 429:
                    print "Waiting. You've probably reached an API limit."
                    time.sleep(5)
            except: 
                print(sys.exc_info())
                continue


# In[44]:

json_file_path = "nytimes/json/"
tsv_file_name = "nytimes/output.csv"
log_file = "nytimes/output.log"
api_key = "51de9d28a17d432786a7985d1aab98bd"
start_date = yesterday if sys.argv[2] == "day" else last_week
end_date = today
query = KEYWORD

try:
    getArticles(start_date, end_date, query, api_key, json_file_path)
    #parseArticles(start_date, csv_file_name, json_file_path)
except:
    print(sys.exc_info())


# In[48]:

a = [json.loads(open(json_file_path+i).readline()) for i in os.listdir(json_file_path)]
snippets = [i["response"]["docs"][j]["snippet"] for i in a for j in range(len(i["response"]["docs"]))]
url = [i["response"]["docs"][j]["web_url"] for i in a for j in range(len(i["response"]["docs"]))]
header = []
p = []
count = 0

#start_time = time.time()
for i in url:
    response = urllib.urlopen(i)
    content = response.read()
    soup = BeautifulSoup(content)
    head = soup.find("h1").text
    if head.strip() == "Donald Trump":
        continue
    header.append(head)
    p.append(" ".join([i.text for i in soup.findAll("p")]))
    count+=1
    print count,
    #print time.time() - start_time
    #start_time = time.time()



pd.DataFrame({"Para":[re.sub(r'[^\x00-\x7f]',r' ', i) for i in p],"Head":[re.sub(r'[^\x00-\x7f]',r' ', i) for i in p]}).to_csv("NYTimes.csv")

with open("nytimes.txt","w") as f:
    f.writelines([re.sub(r'[^\x00-\x7f]',r' ', i) for i in p])
