import json
import pymongo
from tqdm import tqdm

# Connect to Mongo
conex = pymongo.MongoClient()

print(conex.list_database_names())

# Database practica (already created)
db = conex.practica
print(db.list_collection_names())

# Load json
with open('./dblp.json') as json_file:
    json_documents = json.load(json_file)

# Conexión a la base de datos e inserción en la colección de documentos
for k, v in tqdm(json_documents.items()):
    db.documentos.insert_one(v)

print(db.list_collection_names())

# Creación de la colección de autores
pipeline_authors_collection = [{"$unwind": "$authors"},
                               {"$group": {"_id": "$authors", "publications": {"$push": "$_id"}}},
                               {'$out': "autores"}]
db.documentos.aggregate(pipeline_authors_collection,  allowDiskUse = True)

print(db.list_collection_names())