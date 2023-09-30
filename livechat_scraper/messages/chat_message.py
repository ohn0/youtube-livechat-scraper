"""Message output for text messages sent in livechat"""
import livechat_scraper.constants.node_constants as nc
import livechat_scraper.constants.scraper_constants as sCons
from livechat_scraper.messages.fragments.content import Content
from livechat_scraper.messages.fragments.emoji import Emoji
from livechat_scraper.messages.message import Message

class ChatMessage(Message):
    """Class for text message objects from scrape"""
    def build_message(self):
        """grabs text message node from scraped content and pulls out relevant
        data, including the text message sent, the author, and timestamps."""
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE]\
            [nc.ITEM_NODE][nc.LIVECHAT_TEXT_MESSAGE_RENDERER_NODE]
        self.occurrence_timestamp = self.content_node[nc.TIMESTAMP_SIMPLE_TEXT_NODE]\
            [nc.SIMPLE_TEXT_NODE]
        self.time_stamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        if nc.AUTHOR_NODE in self.content_node:
            self.author = self.content_node[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]

        runs = self.content_node[nc.MESSAGE_NODE][nc.RUNS_NODE]
        message = ""
        emojis = []
        text_content = ""
        for run in runs:
            if "emoji" in run:
                emojis.append(Emoji(run[nc.EMOJI_NODE]).get_content())
                message += f"${run[nc.EMOJI_NODE][nc.IMAGE_NODE][nc.ACCESSIBILITY_NODE][nc.ACCESSIBILITY_DATA_NODE][nc.LABEL_NODE]} "
            elif "text" in run:
                text_content += f"{run[nc.TEXT_NODE]} "
                message += f"{run[nc.TEXT_NODE]} "

        self.context_message = {
            "message" : message,
            "emoji" : emojis,
            "text_content" : text_content
        }

    def generate_content(self):
        """outputs the generated message object"""
        return Content(self.occurrence_timestamp, self.time_stamp, self.author,\
             self.context_message, sCons.MESSAGE_TYPE_CHAT).object_output()
             