from messages.fragments.content import Content
from messages.message import Message
from messages.fragments.emoji import Emoji
import constants.node_constants as nc
import constants.scraper_constants as sCons

class chatMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_TEXT_MESSAGE_RENDERER_NODE]
        self.occurrenceTimestamp = self.content_node[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        self.timeStamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        if(nc.AUTHOR_NODE in self.content_node):
            self.author = self.content_node[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.contextMessage = {
            "message" : self.extractText(self.content_node[nc.MESSAGE_NODE][nc.RUNS_NODE]),
            "emoji" : self.extractEmojis(self.content_node[nc.MESSAGE_NODE][nc.RUNS_NODE]) 
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
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage, sCons.MESSAGE_TYPE_CHAT).objectOutput()