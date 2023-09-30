"""Message output for gifted membership redeemed messages sent in livechat"""
from livechat_scraper.messages.message import Message
from livechat_scraper.messages.fragments.content import Content
import livechat_scraper.constants.node_constants as nc
import livechat_scraper.constants.scraper_constants as sCons

class MembershipRedeemedMessage(Message):
    """Class for scraping gifted memberships that are redeemed"""

    def build_message(self):
        """
        builds message for redeemed membership message content
        content consist of the name of the user who got gifted a membership and the 
        name of the gifter
        """
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE]\
            [nc.LIVECHAT_MEMBERSHIP_GIFT_RECEIVED_ANNOUNCEMENT_NODE]
        
        self.time_stamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        self.author = self.content_node[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.context_message = {
            "giftedText" : f"{self.author} {self.runs_message_builder(self.content_node[nc.MESSAGE_NODE][nc.RUNS_NODE])}"
        }
        self.occurrence_timestamp = self.content_node[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]

    def generate_content(self):
        """
        generates the membership gifting received message for consumption 
        """
        return Content(self.occurrence_timestamp,
        self.time_stamp,
        self.author,
        self.context_message,
        sCons.MESSAGE_TYPE_MEMBERSHIP_GIFT_RECEIVED).object_output()