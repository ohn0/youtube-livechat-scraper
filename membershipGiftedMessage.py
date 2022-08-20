from message import Message
from content import Content
import nodeConstants as nc

class membershipGiftedMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.replayActionNode][nc.actionsNode][0]
        [nc.addChatItemActionNode][nc.itemNode][nc.liveChatMembershipGiftPurchasedAnnouncementNode]
        self.timeStamp = self.contentNode[nc.timestampUsecNode]
        self.occurrenceTimestamp = self.action[nc.replayActionNode][nc.videoOffsetTimeMsecNode]
        self.author = self.action[nc.headerNode][nc.liveChatSponsorshipHeaderNode][nc.authorNode][nc.simpleTextNode]
        self.contextMessage = {
            "Gift Text" : self.runsMessageBuilder(self.action[nc.headerNode][nc.primaryTextNode]),
        }

    def generateContent(self):
        return Content(self.occurrenceTimestamp, 
                       self.timeStamp,
                       self.author,
                       self.contextMessage)