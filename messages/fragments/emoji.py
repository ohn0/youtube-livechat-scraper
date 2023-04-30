import constants.node_constants as nc
class Emoji:
    name = ''
    isCustom = False
    imageUrl = ''
    def __init__(self, EMOJI_NODE):
        self.setProperties(EMOJI_NODE)

    def setProperties(self, emoji):
        self.name = emoji[nc.IMAGE_NODE][nc.ACCESSIBILITY_NODE][nc.ACCESSIBILITY_DATA_NODE][nc.LABEL_NODE]
        self.isCustom = nc.CUSTOM_EMOJI_NODE in emoji
        if(self.isCustom):
            self.imageUrl = emoji[nc.IMAGE_NODE][nc.THUMBNAIL_NODE][1][nc.URL_NODE]
        else:
            self.imageUrl = emoji[nc.IMAGE_NODE][nc.THUMBNAIL_NODE][0][nc.URL_NODE]

    def getContent(self):
        return {
            "name" : self.name,
            "isCustom" : self.isCustom,
            "imageUrl" : self.imageUrl
        }