import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient('localhost', 27017)
    print "Connected successfully!!!"
    db = conn['bagiks']
    collection = db.properties
    print collection
    print db.collection_names()
    doc = {"name":"Alberto","surname":"Negron","twitter":"@Altons"}
    collection.insert(doc)
    print collection.count()
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e
conn