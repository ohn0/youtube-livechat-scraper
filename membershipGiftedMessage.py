from message import Message
from content import Content
import nodeConstants as nc

class membershipGiftedMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.addChatItemActionNode][nc.itemNode][nc.liveChatMembershipGiftPurchasedAnnouncementNode]
        self.timeStamp = self.contentNode[nc.timestampUsecNode]
        self.occurrenceTimestamp = self.contentNode[nc.timestampSimpleTextNode][nc.simpleTextNode]
        self.author = self.action[nc.headerNode][nc.liveChatSponsorshipHeaderNode][nc.authorNode][nc.simpleTextNode]
        self.contextMessage = {
            "Gift Text" : self.runsMessageBuilder(self.action[nc.headerNode][nc.primaryTextNode]),
        }

    def generateContent(self):
        return Content(self.occurrenceTimestamp, 
                       self.timeStamp,
                       self.author,
                       self.contextMessage)