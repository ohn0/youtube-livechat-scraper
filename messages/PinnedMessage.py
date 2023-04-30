from messages.message import Message
from messages.fragments.content import Content
import constants.nodeConstants as nc
import constants.scraperConstants as sCons
class PinnedMessage(Message):

    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.CONTENT_NODE = self.action[nc.ADD_BANNER_NODE]
        content = self.CONTENT_NODE[nc.BANNER_RENDERER_NODE][nc.LIVECHAT_BANNER_RENDERER_NODE][nc.CONTENT_NODE][nc.LIVECHAT_TEXT_MESSAGE_RENDERER_NODE]
        header = self.CONTENT_NODE[nc.BANNER_RENDERER_NODE][nc.LIVECHAT_BANNER_RENDERER_NODE][nc.HEADER_NODE]
        self.timeStamp = content[nc.TIMESTAMP_USEC_NODE]
        self.author = ''
        self.occurrenceTimestamp = content[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        runsContent = header[nc.BANNER_HEADER_RENDERER_NODE][nc.TEXT_NODE]
        self.contextMessage = {
                "pinned_by" : self.runsMessageBuilder(runsContent),
                "message" : content[nc.MESSAGE_NODE][nc.RUNS_NODE][0][nc.TEXT_NODE]
        }
    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage, sCons.messageTypePinned).objectOutput()
    
    