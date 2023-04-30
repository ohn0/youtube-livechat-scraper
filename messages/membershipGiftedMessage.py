from messages.message import Message
from messages.fragments.content import Content
import constants.node_constants as nc
import constants.scraperConstants as sCons
class membershipGiftedMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.CONTENT_NODE = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_MEMBERSHIP_GIFT_PURCHASED_ANNOUNCEMENT_NODE]
        self.timeStamp = self.CONTENT_NODE[nc.TIMESTAMP_USEC_NODE]
        self.author = self.CONTENT_NODE[nc.HEADER_NODE][nc.LIVECHAT_SPONSORSHIP_HEADER_NODE][nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.contextMessage = {
            "giftText" : self.runsMessageBuilder(self.CONTENT_NODE[nc.HEADER_NODE][nc.LIVECHAT_SPONSORSHIP_HEADER_NODE][nc.PRIMARY_TEXT_NODE][nc.RUNS_NODE]),
        }

    def generateContent(self):
        return Content(None,
                       self.timeStamp,
                       self.author,
                       self.contextMessage,
                       sCons.messageTypeMembershipGift).objectOutput()