from messages.fragments.content import Content
from messages.message import Message
from messages.fragments.emoji import Emoji
import constants.nodeConstants as nc
import constants.scraperConstants as sCons

class chatMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.CONTENT_NODE = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_TEXT_MESSAGE_RENDERER_NODE]
        self.occurrenceTimestamp = self.CONTENT_NODE[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        self.timeStamp = self.CONTENT_NODE[nc.TIMESTAMP_USEC_NODE]
        if(nc.AUTHOR_NODE in self.CONTENT_NODE):
            self.author = self.CONTENT_NODE[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.contextMessage = {
            "message" : self.extractText(self.CONTENT_NODE[nc.MESSAGE_NODE][nc.RUNS_NODE]),
            "emoji" : self.extractEmojis(self.CONTENT_NODE[nc.MESSAGE_NODE][nc.RUNS_NODE]) 
        }

    def extractEmojis(self, runs):
        emojis = []
        for run in runs:
            if("emoji" in run):
                emojis.append(Emoji(run[nc.EMOJI_NODE]).getContent())
        return emojis

    def extractText(self, runs):
        text = ''
        for run in runs:
            if("text" in run):
                text += run["text"]
        return text
        
    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage, sCons.messageTypeChat).objectOutput()