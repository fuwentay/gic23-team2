## Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred                     
import pymongo
import sys

client = pymongo.MongoClient('mongodb://team2:Lmao=2106@gic-hackathon.cluster-cf4nwjxkqflm.ap-southeast-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=../global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')

##Specify the database to be used
db = client.sample_database

##Specify the collection to be used
col = db.sample_collection

##Insert a single document
col.insert_one({'hello':'Amazon DocumentDB'})

##Find the document that was previously written
x = col.find_one({'hello':'Amazon DocumentDB'})

##Print the result to the screen
print(x)

##Close the connection
client.close()