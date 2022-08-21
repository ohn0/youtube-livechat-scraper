from message import Message
from content import Content
import nodeConstants as nc
class PinnedMessage(Message):

    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.contentNode = self.action[nc.replayActionNode][nc.actionsNode][0][nc.addBannerNode]
        content = self.contentNode[nc.addBannerNode][nc.bannerRendererNode]
        [nc.liveChatBannerRendererNode][nc.contentNode][nc.liveChatTextMessageRendererNode]
        header = self.contentNode[nc.addBannerNode][nc.bannerRendererNode][nc.liveChatBannerRendererNode][nc.headerNode]
        self.occurrenceTimestamp = self.action[nc.replayActionNode][nc.videoOffsetTimeMsecNode]
        self.author = ''
        self.timeStamp = content[nc.timestampSimpleTextNode][nc.simpleTextNode]
        runsContent = header[nc.bannerHeaderRendererNode][nc.textNode]
        self.contextMessage = {
                "pinnedBy" : self.runsMessageBuilder(runsContent),
                "message" : content[nc.messageNode][nc.runsNode][0][nc.textNode]
        }
    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage)
    
    