from messages.message import Message
from messages.fragments.content import Content
import constants.node_constants as nc
import constants.scraper_constants as sCons
class PinnedMessage(Message):

    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.content_node = self.action[nc.ADD_BANNER_NODE]
        content = self.content_node[nc.BANNER_RENDERER_NODE][nc.LIVECHAT_BANNER_RENDERER_NODE][nc.CONTENT_NODE][nc.LIVECHAT_TEXT_MESSAGE_RENDERER_NODE]
        header = self.content_node[nc.BANNER_RENDERER_NODE][nc.LIVECHAT_BANNER_RENDERER_NODE][nc.HEADER_NODE]
        self.timeStamp = content[nc.TIMESTAMP_USEC_NODE]
        self.author = ''
        self.occurrenceTimestamp = content[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        runsContent = header[nc.BANNER_HEADER_RENDERER_NODE][nc.TEXT_NODE]
        self.contextMessage = {
                "pinned_by" : self.runsMessageBuilder(runsContent),
                "message" : content[nc.MESSAGE_NODE][nc.RUNS_NODE][0][nc.TEXT_NODE]
        }
    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage, sCons.MESSAGE_TYPE_PINNED).objectOutput()
    
    