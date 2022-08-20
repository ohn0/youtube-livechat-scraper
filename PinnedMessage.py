from message import Message
from content import Content
import nodeConstants as nc
class PinnedMessage(Message):

    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.replayActionNode][nc.actionsNode][0][nc.addBannerNode]
        self.occurrenceTimestamp = self.action[nc.replayActionNode][nc.videoOffsetTimeMsecNode]
        self.author = ''
        self.timeStamp = self.contentNode[nc.addBannerNode][nc.bannerRendererNode][nc.liveChatBannerRendererNode][nc.contentNode][nc.liveChatTextMessageRendererNode][nc.timestampSimpleTextNode][nc.simpleTextNode]
        runsContent = self.contentNode[nc.addBannerNode][nc.bannerRendererNode][nc.liveChatBannerRendererNode][nc.headerNode][nc.bannerHeaderRendererNode][nc.textNode]
        self.contextMessage = {
                "pinned By Message" : self.runsMessageBuilder(runsContent),
                "pinned message" : self.contentNode[nc.addBannerNode][nc.bannerRendererNode][nc.liveChatBannerRendererNode][nc.contentNode][nc.liveChatTextMessageRendererNode][nc.messageNode][nc.runsNode][0][nc.textNode]
        }
    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage)
    
    