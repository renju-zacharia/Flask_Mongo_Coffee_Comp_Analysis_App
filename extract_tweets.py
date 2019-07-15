# Import dependencies
import twitter
from bs4 import BeautifulSoup
import requests
import pymongo
import pprint
from datetime import datetime, timedelta
# Import program used to categorize sentiments
import sent_rating 
import config as config

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.twitter_db
collection = db.tweets
collection.drop()

api = twitter.Api(consumer_key=config.API_KEY,
  consumer_secret=config.API_SECRET,
  access_token_key=config.ACCESS_TOKEN,
  access_token_secret=config.ACCESS_TOKEN_SECRET)

#print(api.VerifyCredentials())

# Create a search list for companies
search_list = [{"id":"SB","name":"Star Bucks","search_str":'Starbucks Coffee'},
               {"id":"MD","name":"McDonalds","search_str":"McDonald Coffee"},
              {"id":"DD","name":"Dunkin Donuts","search_str":"Dunkin Coffee"}]


# Calculate a date range array with a range starting from current date going  back 10 days
N=10
v_curr_date = datetime.today().strftime('%Y-%m-%d')
v_rng_strt_dt_char =  (datetime.today() - timedelta(days=N)).strftime('%Y-%m-%d')
v_rng_strt_dt = datetime.strptime(v_rng_strt_dt_char,'%Y-%m-%d')
date_arr=[]
for i in range(0,11):
   date_arr.append((v_rng_strt_dt + timedelta(days=i)).strftime('%Y-%m-%d'))

v_lang = "en"
v_count = 1000
v_geo_code = [40.7128, -74.0060, "5000mi"]
v_sentiment=""

for x in search_list:

  for v_strt_dt in date_arr:
    
        query = x['search_str']
        v_id = x['id']
        v_name = x['name']
        
        v_end_dt = (datetime.strptime(v_strt_dt, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    
        search = api.GetSearch(term=query,since=v_strt_dt,until=v_end_dt,lang=v_lang,count=v_count)


        for tweet in search:
            # Error handling
            try:
        
                # Print the output from twitter on the screen
                #print(tweet.id, tweet.text);
                #create_date = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +%f %Y').strftime('%d/%m/%Y')
                create_date = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +%f %Y').strftime('%Y-%m-%d')
                print(f'Create Date: {create_date} Rng_Str: {v_strt_dt} Rng_End: {v_end_dt}')
            
                v_sentiment = sent_rating.get_rating(tweet.text);
                
              
            
                # Dictionary to be inserted as a MongoDB document
                post = {
                    'id': v_id,
                    'name': v_name,
                    'created' : create_date,
                    'range_strt_dt': v_strt_dt,
                    'range_end_dt' : v_end_dt,
                    'search_str': query,
                    'tweet_id': tweet.id,
                    'tweet_text': tweet.text,
                    'retweet_count': tweet.retweet_count,
                    'source' : tweet.source,
                    'favourite_count' : tweet.user.favourites_count,
                    'sentiment' : v_sentiment
                }

                collection.insert_one(post)

            except Exception as e:
                print(e)
        #print(tweet.id);

##Checking the load into mongo db

# Display items in MongoDB collection
tweet_recs = db.tweets.find()

#for tweet in tweet_recs:
#    print(tweet)

db.tweets.count() 

y=db.tweets.aggregate([
{ "$group": { "_id": "$name", "No_of_Times": { "$sum": 1 } } }
])

for t in y:
    print(t)

