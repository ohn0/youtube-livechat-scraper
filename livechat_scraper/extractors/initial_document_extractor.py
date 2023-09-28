"""module for extracting initial start up content from first post request."""
import json

from bs4 import BeautifulSoup

class InitialExtractor:
    """class to extract initial values from first POST request"""
    parse_type = ''
    def __init__(self):
        self.parse_type = 'html.parser'

    def build_and_get_script(self, data):
        """parses response contents and returns portion where livechat data resides."""
        parser = BeautifulSoup(data, self.parse_type)
        scripts = parser.find_all('script')
        content = str([x for x in scripts if "endTimestamp" in x.text][0])
        start_index = content.find('{')
        end_index = len(content) - content[::-1].find('}')
        # with open ('output/InitialExtractor.json', 'w', encoding='utf-8') as writer:
        #     writer.write(str(json.loads(content[start_index:end_index])))
        return json.loads(content[start_index:end_index])
