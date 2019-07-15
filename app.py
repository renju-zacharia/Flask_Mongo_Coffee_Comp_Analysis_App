from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import pymongo
# import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/twitter_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    tweets_rec = mongo.db.tweets.find_one()

    #print(tweets_rec)
   
    # Return index.html
    return render_template("index.html")
 
# Route that will return aggregated sentiments counts
@app.route("/rating/<cmp>/")
def rating(cmp):

    #Aggregate from Mongodb
    tweets_rec = list(mongo.db.tweets.aggregate(
                 [ 
                    { "$match": { 'id': cmp } },
                    { "$group": { '_id': "$sentiment" , "No_of_Times": { "$sum": 1 } } },
                    { "$sort" : { '_id' : -1 } }
                 ]
        ))

    sentiments_list = []
    ratings_list = []

    for tweet in tweets_rec:
        sentiments_list.append(tweet['_id'])
        ratings_list.append(tweet['No_of_Times'])

    return_json =  { 
                     "company" : cmp , 
                     "sentiments" : sentiments_list, 
                     "ratings" : ratings_list
                   }

    #Return json 
    print(return_json)
    return jsonify(return_json)

# Route that will return aggregated tweet counts
@app.route("/tweets/<cmp>/")
def tweets(cmp):

    #Aggregate from Mongodb
    tweets_rec = list(mongo.db.tweets.aggregate(
                 [ 
                    { "$match": { 'id': cmp } },
                    { "$group": { '_id': "$sentiment" , "No_of_Times": { "$sum": 1 } } },
                    { "$sort" : { '_id' : -1 } }
                 ]
        ))

    sentiments_list = []
    ratings_list = []

    for tweet in tweets_rec:
        sentiments_list.append(tweet['_id'])
        ratings_list.append(tweet['No_of_Times'])

    return_json =  { 
                     "company" : cmp , 
                     "sentiments" : sentiments_list, 
                     "ratings" : ratings_list
                   }

    #Return json 
    return jsonify(return_json)
# Route that will return aggregated tweet counts
@app.route("/retweets/<cmp>/")
def retweets(cmp):

    #Aggregate from Mongodb
    retweets_rec = list(mongo.db.tweets.aggregate(
                 [ 
                    { "$match": { 'id': cmp } },
                    { "$group": { "_id": "$sentiment", "No_of_Times": { "$sum": "$retweet_count" } } },
                    { "$sort" : { '_id' : -1 } }
                 ]
        ))

    sentiments_list = []
    retweet_list = []

    for retweet in retweets_rec:
        sentiments_list.append(retweet['_id'])
        retweet_list.append(retweet['No_of_Times'])

    return_json =  { 
                     "company" : cmp , 
                     "sentiments" : sentiments_list, 
                     "retweets" : retweet_list
                   }
    #print(return_json)
    #Return json 
    return jsonify(return_json)
# Route that will return recent tweets
@app.route("/metadata/<cmp>/")
def metadata(cmp):

    sample_metadata = {}

    metadata_rec = mongo.db.tweets.find( { 'id': cmp } ).sort([("created", -1)]).limit(3)
    i=1
    for tweet in metadata_rec:        
        tim=tweet['created']        
        #sample_metadata[tim] = tweet['tweet_text']   
        sample_metadata[i] = tweet['created'] + ' ::: ' + tweet['tweet_text']
        i = i + 1;     
    
    return jsonify(sample_metadata)

# Route that will plot revenue and store count charts
@app.route("/sales/<cmp>")
def sales(cmp):

   sales_rec = mongo.db.sales.find_one()
   year_list = []
   rev_list = []
   store_list = []
   for record in sales_rec[cmp]:
       year_list.append(record['year'])
       rev_list.append(record['revenue'])
       store_list.append(record['stores'])
   return_json =  {
                   "company": cmp,
                   "year": year_list,
                   "stores": store_list,
                   "revenue": rev_list
   }

   return jsonify(return_json)

#Route that adds up Retweets by company 
@app.route("/retwtcnt/<cmp>/")
def retwtcnt(cmp):
    
    #Aggregate from Mongodb
    tweets_rec = list(mongo.db.tweets.aggregate(
                 [ 
                    { "$match": { 'id': cmp } },
                    { "$group": { '_id': 'null' , "No_of_Retweets": { "$sum": "$retweet_count" } } },
                    { "$sort" : { '_id' : -1 } }
                 ]
        ))

    retweets_list = []

    for tweet in tweets_rec:
        retweets_list.append(tweet['No_of_Retweets'])        

    return_json =  { 
                     "company" : cmp , 
                     "retweet_count" : retweets_list
                   }

    #Return json 
    #print (jsonify(return_json))

    return jsonify(return_json)
if __name__ == "__main__":
    app.run(debug=True)
