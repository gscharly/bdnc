from pymongo import MongoClient
import json

# Connect to Mongo
conex = MongoClient()

print(conex.list_database_names())
# Database practica (already created)
db = conex.practica
# print(db.list_collection_names())
# Create collection
col = db.Publications

# Load json
with open("dblp.json", encoding='utf-8') as json_data:
    data = json.load(json_data)
# json_dict = json.loads('dblp.json')
# Insert
print(type(data))

for k, v in data.items():
    col.insert_one(v)

# col.insert_one(data)

print(db.list_collection_names())