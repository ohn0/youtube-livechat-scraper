"""module ofr processing a superchat message from scraper"""
import livechat_scraper.constants.node_constants as nc
import livechat_scraper.constants.scraper_constants as sCons
from livechat_scraper.messages.fragments.content import Content
from livechat_scraper.messages.message import Message

class SuperChatMessage(Message):
    """class for processing a superchat object into a message
    for consumption"""

    def build_message(self):
        """converts a superchat message from scraper content
        into a message object for consumption"""
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE]\
            [nc.LIVECHAT_PAID_MESSAGE_NODE]
        self.occurrence_timestamp = self.content_node[nc.TIMESTAMP_SIMPLE_TEXT_NODE]\
            [nc.SIMPLE_TEXT_NODE]
        self.time_stamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        self.author = self.content_node[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.context_message = {
            "purchaseAmount" : self.content_node[nc.PURCHASE_AMOUNT_NODE],
            "message" : self.runs_message_builder(self.content_node[nc.MESSAGE_NODE]\
                [nc.RUNS_NODE]) if nc.MESSAGE_NODE in self.content_node else ''
        }

    def generate_content(self):
        """generates superchat message output for consumption"""
        return Content(
            self.occurrence_timestamp,
            self.time_stamp,
            self.author,
            self.context_message,
            sCons.MESSAGE_TYPE_SUPER_CHAT
        ).object_output()
