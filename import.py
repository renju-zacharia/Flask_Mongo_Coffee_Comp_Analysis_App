import csv
import os
import pymongo




myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["twitter_db"]
mycol = mydb["sales"]
mycol.drop()
salesCSV = os.path.join('.', 'data', 'sales.csv')
dict_rec = {}
with open(salesCSV, 'r') as csvfile:

    # Split the data on commas
    csvreader = csv.reader(csvfile, delimiter=',')

    header = next(csvreader)
   

    
    # Loop through the data
    for row in csvreader:
        
        if not row[0] in dict_rec:
            dict_rec[row[0]]=[]
        dict_rec[row[0]].append(
            {"year": row[1],
            "revenue": row[2],
            "stores": row[3]})
   
x = mycol.insert_one(dict_rec)


#print(dict_rec)

        