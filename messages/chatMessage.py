from content import Content
from messages.message import Message
from emoji import Emoji
import nodeConstants as nc
import scraperConstants as sCons

class chatMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.addChatItemActionNode][nc.itemNode][nc.liveChatTextMessageRendererNode]
        self.occurrenceTimestamp = self.contentNode[nc.timestampSimpleTextNode][nc.simpleTextNode]
        self.timeStamp = self.contentNode[nc.timestampUsecNode]
        if(nc.authorNode in self.contentNode):
            self.author = self.contentNode[nc.authorNode][nc.simpleTextNode]
        self.contextMessage = {
            "message" : self.extractText(self.contentNode[nc.messageNode][nc.runsNode]),
            "emoji" : self.extractEmojis(self.contentNode[nc.messageNode][nc.runsNode]) 
        }

    def extractEmojis(self, runs):
        emojis = []
        for run in runs:
            if("emoji" in run):
                emojis.append(Emoji(run[nc.emojiNode]).getContent())
        return emojis

    def extractText(self, runs):
        text = ''
        for run in runs:
            if("text" in run):
                text += run["text"]
        return text
        
    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage, sCons.messageTypeChat).objectOutput()