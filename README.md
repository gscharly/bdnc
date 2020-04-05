# Práctica 1 Base de datos no convencionales

## Ejecución

### Procesado de XML
En primer lugar, se cambia la codificación del XML original a UTF-8. Para ello, 
se utiliza el script **xml_to_utf.py**, que lee el fichero comprimido original
(dblp.xml.gz).

### Creación de JSON
El segundo paso es la creación del fichero JSON a partir del XML procesado. Para
ello, se usa el script **xml_to_json.py** sobre el resultado del anterior paso 
(una vez descomprimido).

### Creación de base de datos en Mongo DB
A continuación, se procede a crear la base de datos en mongo, incluyendo dos 
colecciones: autores y publicaciones. Para ello, se puede usar el notebook 
**create_collections.ipynb** o el script **create_collections.py**, que leerán
el resultado del paso anterior del fichero **dblp.json**. 