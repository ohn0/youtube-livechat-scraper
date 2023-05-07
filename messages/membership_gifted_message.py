"""Message output for gifted membership messages sent in livechat"""
from messages.message import Message
from messages.fragments.content import Content
import constants.node_constants as nc
import constants.scraper_constants as sCons
class MembershipGiftedMessage(Message):
    """Class for membership gifted message objects from scrape"""
    def build_message(self):
        """builds membership gifted message from scraped content
        content of the message consists of membership gifted message and
        metadata."""
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE]\
            [nc.LIVECHAT_MEMBERSHIP_GIFT_PURCHASED_ANNOUNCEMENT_NODE]
        self.time_stamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        self.author = self.content_node[nc.HEADER_NODE][nc.LIVECHAT_SPONSORSHIP_HEADER_NODE]\
            [nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.context_message = {
            "giftText" : self.runs_message_builder(self.content_node[nc.HEADER_NODE]\
                [nc.LIVECHAT_SPONSORSHIP_HEADER_NODE][nc.PRIMARY_TEXT_NODE][nc.RUNS_NODE]),
        }

    def generate_content(self):
        """generates the membership gifted message object for
        output consumption."""
        return Content(None,
                       self.time_stamp,
                       self.author,
                       self.context_message,
                       sCons.MESSAGE_TYPE_MEMBERSHIP_GIFT).object_output()
