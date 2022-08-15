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
        content = str([x for x in scripts if "endTimeMs" in x.text][0])
        startIndex = content.find('{')
        endIndex = len(content) - content[::-1].find('}')
        jsonContents = json.loads(content[startIndex:endIndex])
        return jsonContents


# htmlContent = ''
# with open('z.html', 'r', encoding='utf-8') as reader:
#     for line in reader:
#         htmlContent += line
# # print(htmlContent)
# ex = initialExtractor()
# azfw= ex.buildAndGetScript(htmlContent)
# print(azfw["annotations"][0]["playerAnnotationsExpandedRenderer"]["featuredChannel"]["endTimeMs"])