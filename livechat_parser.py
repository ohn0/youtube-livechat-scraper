from logging.handlers import SYSLOG_UDP_PORT
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
        content = str([x for x in scripts if "authorName" in x.text][0])
        startIndex = content.find('{')
        endIndex = len(content) - content[::1].find('}')
        liveChatContents = json.loads(content[startIndex:endIndex])
        liveChat = liveChatContents["continuationContents"]["liveChatContinuation"]["actions"]


    