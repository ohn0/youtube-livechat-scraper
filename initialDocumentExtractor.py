from cgitb import html
from bs4 import BeautifulSoup
import json

class initialExtractor:
    parseType = ''
    def __init__(self):
        self.parseType = 'html.parser'

    def buildAndGetScript(self, data):
        parser = BeautifulSoup(data, self.parseType)
        scripts = parser.find_all('script')
        content = str([x for x in scripts if "endTimestamp" in x.text][0])
        startIndex = content.find('{')
        endIndex = len(content) - content[::-1].find('}')
        jsonContents = json.loads(content[startIndex:endIndex])
        # with open ('output/initialExtractor.json', 'w', encoding='utf-8') as writer:
        #     writer.write(str(jsonContents))
        return jsonContents