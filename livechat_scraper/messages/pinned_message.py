"""module for processing pinned scraped messages"""
import livechat_scraper.constants.node_constants as nc
import livechat_scraper.constants.scraper_constants as sCons
from livechat_scraper.messages.fragments.content import Content
from livechat_scraper.messages.message import Message

class PinnedMessage(Message):
    """class for taking a pinned message and converting it to a
    message object for consumption"""

    def build_message(self):
        """builds a pinned message for output from a given livechat
        pinned message"""
        self.content_node = self.action[nc.ADD_BANNER_NODE]
        content = self.content_node[nc.BANNER_RENDERER_NODE][nc.LIVECHAT_BANNER_RENDERER_NODE]\
            [nc.CONTENT_NODE][nc.LIVECHAT_TEXT_MESSAGE_RENDERER_NODE]
        header = self.content_node[nc.BANNER_RENDERER_NODE][nc.LIVECHAT_BANNER_RENDERER_NODE]\
            [nc.HEADER_NODE]
        self.time_stamp = content[nc.TIMESTAMP_USEC_NODE]
        self.author = ''
        self.occurrence_timestamp = content[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        content = header[nc.BANNER_HEADER_RENDERER_NODE][nc.TEXT_NODE]
        self.context_message = {
                "pinned_by" : self.runs_message_builder(content),
                "message" : content[nc.MESSAGE_NODE][nc.RUNS_NODE][0][nc.TEXT_NODE]
        }

    def generate_content(self):
        """generates pinned message output"""
        return Content(self.occurrence_timestamp, self.time_stamp, self.author, self.context_message, sCons.MESSAGE_TYPE_PINNED).object_output()
    