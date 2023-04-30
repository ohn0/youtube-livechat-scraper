from messages.message import Message
from messages.fragments.content import Content
import constants.node_constants as nc
import constants.scraper_constants as sCons
class membershipGiftedMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_MEMBERSHIP_GIFT_PURCHASED_ANNOUNCEMENT_NODE]
        self.timeStamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        self.author = self.content_node[nc.HEADER_NODE][nc.LIVECHAT_SPONSORSHIP_HEADER_NODE][nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.contextMessage = {
            "giftText" : self.runsMessageBuilder(self.content_node[nc.HEADER_NODE][nc.LIVECHAT_SPONSORSHIP_HEADER_NODE][nc.PRIMARY_TEXT_NODE][nc.RUNS_NODE]),
        }

    def generateContent(self):
        return Content(None,
                       self.timeStamp,
                       self.author,
                       self.contextMessage,
                       sCons.MESSAGE_TYPE_MEMBERSHIP_GIFT).objectOutput()