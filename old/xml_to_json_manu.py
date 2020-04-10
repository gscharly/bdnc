import xml.sax
import json
from xml.sax.saxutils import unescape


class DataHandler( xml.sax.ContentHandler ):

    def __init__(self):
        self.json_dict = dict()
        self.author_name = ''
        self.authors = []
        self.title = ''
        self.year = ''
        self.type = ''
        self.key = ''
        self.CurrentData = ''
        self.document_types = ['article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'masterthesis', 'www']
        self.allowed_documents = ['article', 'inproceedings', 'incollection']
        self.document_count = 0

    # Call when an element starts
    def startElement(self, tag, attributes):
        if tag in self.document_types:
            print(len(self.authors))
            self.write_dictionary(self.json_dict)
            self.type = tag
            self.key = attributes['key']
            self.authors = []
        self.CurrentData = tag
        print(self.CurrentData)

    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == 'author':
            self.authors.append(self.author_name)
            self.author_name = ''
        self.CurrentData = ''

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == 'author':
            self.author_name = self.author_name + unescape(content)
        elif self.CurrentData == 'title':
            self.title = content
        elif self.CurrentData == 'year':
            self.year = content

    def write_dictionary(self, dict):
        [print(autor) for autor in self.authors]
        if self.type in self.allowed_documents:
            dict[self.key] = {'authors': self.authors,
                             'title': self.title,
                             'year': self.year,
                             'type': self.type}
            self.document_count += 1
        print('El número de documentos añadidos al json es: {}'.format(self.document_count))



if ( __name__ == "__main__"):

    json_path = './data/dblp.json'
    xml_path = './data/dblp.xml'

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = DataHandler()
    parser.setContentHandler(Handler)

    parser.parse(xml_path)

    json_file = Handler.json_dict

    with open(json_path, 'w') as fp:
        json.dump(json_file, fp, ensure_ascii=False)
