"""Message output for paid membership stickers sent in livechat"""
from livechat_scraper.messages.message import Message
from livechat_scraper.messages.fragments.content import Content
import livechat_scraper.constants.node_constants as nc
import livechat_scraper.constants.scraper_constants as sCons

class PurchasedSticker(Message):
    """Class for handling purchased sticker nodes"""

    def build_message(self):
        """
        builds message for purcahsed sticker content
        content consists of the name of the purchaser, the purchase amount 
        and the sticker description they bought.
        """
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_PAID_STICKER_RENDERER]
        self.time_stamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        self.author = self.content_node[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.occurrence_timestamp = self.content_node[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        self.context_message = {
            "sticker_description" : self.content_node["sticker"][nc.ACCESSIBILITY_NODE][nc.ACCESSIBILITY_DATA_NODE][nc.LABEL_NODE],
            "purchase_amount" : self.content_node[nc.PURCHASE_AMOUNT_NODE][nc.SIMPLE_TEXT_NODE]
        }

    def generate_content(self):
        """generates purchased sticker message"""
        return Content(
            self.occurrence_timestamp,
            self.time_stamp,
            self.author,
            self.context_message,
            sCons.MESSAGE_TYPE_PURCHASED_STICKER
        ).object_output()