from messages.message import Message
from content import Content
import nodeConstants as nc
import scraperConstants as sCons

class superchatMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.addChatItemActionNode][nc.itemNode][nc.liveChatPaidMessageNode]
        self.occurrenceTimestamp = self.contentNode[nc.timestampSimpleTextNode][nc.simpleTextNode]
        self.timeStamp = self.contentNode[nc.timestampUsecNode]
        self.author = self.contentNode[nc.authorNode][nc.simpleTextNode]
        self.contextMessage = {
            "purchaseAmount" : self.contentNode[nc.purchaseAmountNode],
            "message" : self.runsMessageBuilder(self.contentNode[nc.messageNode][nc.runsNode]) if nc.messageNode in self.contentNode else ''
        }

    def generateContent(self):
        return Content(
            self.occurrenceTimestamp,
            self.timeStamp,
            self.author,
            self.contextMessage,
            sCons.messageTypeSuperChat
        ).objectOutput()
