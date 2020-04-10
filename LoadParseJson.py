import ijson
from ijson.common import ObjectBuilder
import pymongo

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


# Conexión al servidor local de mongodb
conex = pymongo.MongoClient()
conex.list_database_names()
db = conex.practica

# Cargamos el fichero json de documentos
for key, value in objects(open('dblp.json', 'rb')):
    db.pruebaparse.insert_one(value)


