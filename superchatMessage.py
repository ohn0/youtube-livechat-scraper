from message import Message
from content import Content
import nodeConstants as nc

class superchatMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.replayActionNode][nc.actionsNode][0]
        livechatNode = self.contentNode[nc.addChatItemActionNode][nc.itemNode][nc.liveChatPaidMessageNode]
        self.occurrenceTimestamp = livechatNode[nc.timestampSimpleTextNode][nc.simpleTextNode]
        self.timeStamp = livechatNode[nc.timestampUsecNode]
        self.author = livechatNode[nc.authorNode][nc.simpleTextNode]
        self.contextMessage = {
            "purchase amount" : livechatNode[nc.purchaseAmountNode],
            "message" : self.runsMessageBuilder(livechatNode[nc.messageNode][nc.runsNode])
        }
