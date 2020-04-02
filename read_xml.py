import json
import lxml.etree as ET
import unidecode
from tqdm import tqdm


def parse_xml(file_name):
    """
    Reads and process xml using lxml. The result is saved in json_path
    :param file_name:
    :param json_path:
    :return:
    """
    events = ("start", "end")
    has_start = False
    json_dict = dict()
    # Traverse the XML
    for event, element in tqdm(ET.iterparse(file_name, events=events, encoding="utf-8", load_dtd=True, recover=True)):
        # print(event, element.tag, element.text)
        # Article node: initialize variables
        if event == 'start' and element.tag in ['article', 'improceedings', 'incollection']:
            has_start = True
            # Each article node has an unique attribute key
            publication_key = element.attrib['key']
            authors = list()
            publication_year = ''
            publication_type = str(element.tag)
            publication_title = ''
        # Author node
        elif event == 'start' and element.tag == 'author' and has_start:
            no_accent = lambda x: unidecode.unidecode(x) if x is not None else x
            authors.append(no_accent(element.text))
        # Title node
        elif event == 'start' and element.tag == 'title' and has_start:
            publication_title = element.text
        # Year node
        elif event == 'start' and element.tag == 'year' and has_start:
            publication_year = element.text
        # End article node: save information. This will never execute before initializing all of the variables
        elif has_start and event == 'end' and element.tag in ['article', 'improceedings', 'incollection']:
            json_dict[publication_key] = {
                '_id': publication_key,
                'authors': authors,
                'title': publication_title,
                'year': publication_year,
                'type': publication_type}
            has_start = False
            element.clear()
        else:
            # Remove element (otherwise there will be memory issues due to file size)
            element.clear()
            continue

    return json_dict


if __name__ == "__main__":
    json_path = 'dblp.json'
    xml_path = 'dblp_final.xml'
    json_dict = parse_xml(xml_path)
    # Write to json
    with open(json_path, 'w', encoding='utf-8') as fp:
        json.dump(json_dict, fp, ensure_ascii=False)





