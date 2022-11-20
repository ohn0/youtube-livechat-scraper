from messages.message import Message
from content import Content
import nodeConstants as nc
import scraperConstants as sCons
class membershipGiftedMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.addChatItemActionNode][nc.itemNode][nc.liveChatMembershipGiftPurchasedAnnouncementNode]
        self.timeStamp = self.contentNode[nc.timestampUsecNode]
        self.author = self.contentNode[nc.headerNode][nc.liveChatSponsorshipHeaderNode][nc.authorNode][nc.simpleTextNode]
        self.contextMessage = {
            "giftText" : self.runsMessageBuilder(self.contentNode[nc.headerNode][nc.liveChatSponsorshipHeaderNode][nc.primaryTextNode][nc.runsNode]),
        }

    def generateContent(self):
        return Content(None,
                       self.timeStamp,
                       self.author,
                       self.contextMessage,
                       sCons.messageTypeMembershipGift).objectOutput()