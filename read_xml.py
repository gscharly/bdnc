import json
import lxml.etree as ET


def parse_xml(file_name, json_path):
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
    for event, element in ET.iterparse(file_name, events=events, recover=True):
        # print(event, element.tag, element.text)
        # print(has_start)
        # Article node: initialize variables
        if event == 'start' and element.tag in ['article', 'improceedings', 'incollection']:
            has_start = True
            # json_dict = dict()
            authors = list()
            publication_year = ''
            publication_type = str(element.tag)
            publication_title = ''
            publication_url = ''
        # Author node
        elif event == 'start' and element.tag == 'author' and has_start:
            authors.append(element.text)
        # Title node
        elif event == 'start' and element.tag == 'title' and has_start:
            publication_title = element.text
        # Year node
        elif event == 'start' and element.tag == 'year' and has_start:
            publication_year = element.text
        # URL node
        elif event == 'start' and element.tag == 'url' and has_start:
            publication_url = element.text
        # End article node: save information. This will never execute before initializing all of the variables
        elif has_start and event == 'end' and element.tag in ['article', 'improceedings', 'incollection']\
                and len(authors) > 0:
            json_dict[publication_url] = {'authors': authors,
                                          'title': publication_title,
                                          'year': publication_year,
                                          'type': publication_type}
            has_start = False
            # with open(json_path, 'w') as fp:
            #     json.dump(json_dict, fp)
        else:
            # Remove element (otherwise there will be memory issues due to file size)
            element.clear()
            continue
    # Write to json
    with open(json_path, 'w') as fp:
        json.dump(json_dict, fp)


if __name__ == "__main__":
    json_path = 'dblp.json'
    xml_path = 'dblp.xml'
    parse_xml(xml_path, json_path)






