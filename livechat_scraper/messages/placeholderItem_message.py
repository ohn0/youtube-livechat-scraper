from livechat_scraper.messages.message import Message
from livechat_scraper.messages.fragments.content import Content
import livechat_scraper.constants.node_constants as nc
import livechat_scraper.constants.scraper_constants as sCons


class PlaceholderItem(Message):
    def build_message(self):
        """
        builds a placeholder message that exists in the livechat
        the placeholder doesnt seem to contain any chat data though.
        all we can grab is the timestamp
        """
        content = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_PLACEHOLDER_ITEM_RENDERER]
        self.occurrence_timestamp = content[nc.TIMESTAMP_USEC_NODE]
        self.context_message = {
            "message" : "placeholder content"
        }

    def generate_content(self):
        """generates a placeholder message"""
        return Content(
            self.occurrence_timestamp,
            self.occurrence_timestamp,
            "N/A",
            self.context_message,
            sCons.MESSAGE_TYPE_PLACEHOLDER_ITEM
        ).object_output()
