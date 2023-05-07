from messages.message import Message
from messages.fragments.content import Content
import constants.node_constants as nc
import constants.scraper_constants as sCons

class SuperChatMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def build_message(self):
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_PAID_MESSAGE_NODE]
        self.occurrence_timestamp = self.content_node[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        self.time_stamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        self.author = self.content_node[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.context_message = {
            "purchaseAmount" : self.content_node[nc.PURCHASE_AMOUNT_NODE],
            "message" : self.runs_message_builder(self.content_node[nc.MESSAGE_NODE][nc.RUNS_NODE]) if nc.MESSAGE_NODE in self.content_node else ''
        }

    def generate_content(self):
        return Content(
            self.occurrence_timestamp,
            self.time_stamp,
            self.author,
            self.context_message,
            sCons.MESSAGE_TYPE_SUPER_CHAT
        ).object_output()