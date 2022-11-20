from messages.message import Message
from messages.fragments.content import Content
import constants.nodeConstants as nc
import constants.scraperConstants as sCons
class PinnedMessage(Message):

    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.addBannerNode]
        content = self.contentNode[nc.bannerRendererNode][nc.liveChatBannerRendererNode][nc.contentNode][nc.liveChatTextMessageRendererNode]
        header = self.contentNode[nc.bannerRendererNode][nc.liveChatBannerRendererNode][nc.headerNode]
        self.timeStamp = content[nc.timestampUsecNode]
        self.author = ''
        self.occurrenceTimestamp = content[nc.timestampSimpleTextNode][nc.simpleTextNode]
        runsContent = header[nc.bannerHeaderRendererNode][nc.textNode]
        self.contextMessage = {
                "pinned_by" : self.runsMessageBuilder(runsContent),
                "message" : content[nc.messageNode][nc.runsNode][0][nc.textNode]
        }
    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage, sCons.messageTypePinned).objectOutput()
    
    