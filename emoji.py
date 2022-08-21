import nodeConstants as nc
class Emoji:
    name = ''
    isCustom = False
    imageUrl = ''
    def __init__(self, emojiNode):
        self.setProperties(emojiNode)

    def setProperties(self, emoji):
        self.name = emoji[nc.imageNode][nc.accessibilityNode][nc.accessibilityDataNode][nc.labelNode]
        self.isCustom = emoji[nc.customEmojiNode] == "true"
        self.imageUrl = emoji[nc.imageNode][nc.thumbnailNode][1][nc.urlNode]
