"""module for Emoji message output creation and handling"""
import livechat_scraper.constants.node_constants as nc
class Emoji:
    """Emoji class to handle parsing emoji messages"""
    def __init__(self, emoji_node):
        self.name = ''
        self.is_custom = False
        self.image_url = ''
        self.__set_properties(emoji_node)

    def __set_properties(self, emoji):
        self.name = emoji[nc.IMAGE_NODE][nc.ACCESSIBILITY_NODE]\
            [nc.ACCESSIBILITY_DATA_NODE][nc.LABEL_NODE]
        self.is_custom = nc.CUSTOM_EMOJI_NODE in emoji
        if self.is_custom:
            self.image_url = emoji[nc.IMAGE_NODE][nc.THUMBNAIL_NODE][1][nc.URL_NODE]
        else:
            self.image_url = emoji[nc.IMAGE_NODE][nc.THUMBNAIL_NODE][0][nc.URL_NODE]

    def get_content(self):
        """returns a constructed emoji object for adding to output"""
        return {
            "name" : self.name,
            "isCustom" : self.is_custom,
            "imageUrl" : self.image_url
        }
        