from bs4 import BeautifulSoup
import json

class livechatParser:
    parseType = ""
    soupParser = None
    liveChatContents = None

    def __init__(self, ParseType):
        self.parseType = ParseType
    
    def buildParser(self, liveChatData):
        self.soupParser = BeautifulSoup(liveChatData.text, self.parseType)

    def findContent(self):
        scripts = self.soupParser.find_all('script')
        content = str([x for x in scripts if "authorName" in x.text][0])
        startIndex = content.find('{')
        endIndex = len(content) - content[::-1].find('}')
        self.liveChatContents = json.loads(content[startIndex:endIndex])
        self.initialContinuation = self.liveChatContents["continuationContents"]["liveChatContinuation"]["header"]["liveChatHeaderRenderer"]["viewSelector"]["sortFilterSubMenuRenderer"]["subMenuItems"][1]["continuation"]["reloadContinuationData"]["continuation"]
        return self.liveChatContents["continuationContents"]["liveChatContinuation"]["actions"]

    



    