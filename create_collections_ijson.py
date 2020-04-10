import ijson
from ijson.common import ObjectBuilder
import pymongo
from tqdm import tqdm


def objects(file):
    key = '-'
    for prefix, event, value in ijson.parse(file):
        if prefix == '' and event == 'map_key':  # found new object at the root
            key = value  # mark the key value
            builder = ObjectBuilder()
        elif prefix.startswith(key):  # while at this key, build the object
            builder.event(event, value)
            if event == 'end_map':  # found the end of an object at the current key, yield
                yield key, builder.value


# Connect to Mongo
conex = pymongo.MongoClient()

print(conex.list_database_names())

# Database practica (already created)
db = conex.practica
print(db.list_collection_names())

# Cargamos el fichero json de documentos
for key, value in tqdm(objects(open('dblp.json', 'rb'))):
    db.documentos.insert_one(value)

print(db.list_collection_names())

# Creación de la colección de autores
pipeline_authors_collection = [{"$unwind": "$authors"},
                               {"$group": {"_id": "$authors", "publications": {"$push": "$_id"}}},
                               {'$out': "autores"}]
db.documentos.aggregate(pipeline_authors_collection,  allowDiskUse=True)

print(db.list_collection_names())