from messages.message import Message
from messages.fragments.content import Content
import constants.nodeConstants as nc
import constants.scraperConstants as sCons

class superchatMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.CONTENT_NODE = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_PAID_MESSAGE_NODE]
        self.occurrenceTimestamp = self.CONTENT_NODE[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        self.timeStamp = self.CONTENT_NODE[nc.TIMESTAMP_USEC_NODE]
        self.author = self.CONTENT_NODE[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.contextMessage = {
            "purchaseAmount" : self.CONTENT_NODE[nc.PURCHASE_AMOUNT_NODE],
            "message" : self.runsMessageBuilder(self.CONTENT_NODE[nc.MESSAGE_NODE][nc.RUNS_NODE]) if nc.MESSAGE_NODE in self.CONTENT_NODE else ''
        }

    def generateContent(self):
        return Content(
            self.occurrenceTimestamp,
            self.timeStamp,
            self.author,
            self.contextMessage,
            sCons.messageTypeSuperChat
        ).objectOutput()
