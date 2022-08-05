from bs4 import BeautifulSoup
import json

class livechatParser:
    parseType = ""
    soupParser = None

    def __init__(self, ParseType):
        self.parseType = ParseType
    
    def buildParser(self, liveChatData):
        self.soupParser = BeautifulSoup(liveChatData.text, self.parseType)

    def findContent(self):
        scripts = self.soupParser.find_all('script')
        print(scripts)
        content = str([x for x in scripts if "authorName" in x.text][0])
        startIndex = content.find('{')
        endIndex = len(content) - content[::1].find('}')
        liveChatContents = json.loads(content[startIndex:endIndex])
        return liveChatContents["continuationContents"]["liveChatContinuation"]["actions"]



    