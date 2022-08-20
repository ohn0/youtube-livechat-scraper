from message import Message
from content import Content
import nodeConstants as nc
class membershipChatMessage(Message):
    membershipDurationHeader = ''
    MESSAGE_TYPES = {"chatMessage": "MEMBERSHIP_CHAT", 
                     "joinMessage" : "MEMBERSHIP_JOINED"}
    MESSAGE_TYPE = None
    def __init__(self, chatAction):
        super().__init__(chatAction)

    def findMembershipMessageType(self):
        if(nc.accessibilityNode in self.action
                [nc.replayActionNode][nc.actionsNode][0][nc.itemNode][nc.tickerItemActionNode]
                [nc.itemNode][nc.liveChatTickerSponsorNode][nc.detailTextNode]):
            self.MESSAGE_TYPE = self.MESSAGE_TYPES["chatMessage"]
        elif(nc.runsNode in self.action
                [nc.replayActionNode][nc.actionsNode][0][nc.itemNode][nc.tickerItemActionNode]
                [nc.itemNode][nc.liveChatTickerSponsorNode][nc.detailTextNode]):
            self.MESSAGE_TYPE = self.MESSAGE_TYPES["joinMessage"]

    def buildMessage(self):
        self.contentNode = self.action[nc.replayActionNode][nc.actionsNode][0][nc.itemNode]
        [nc.tickerItemActionNode][nc.itemNode][nc.liveChatTickerSponsorNode]
        [nc.showItemEndpointNode][nc.showLiveChatEndpointNode][nc.liveChatMembershipNode]
        self.occurrenceTimestamp = self.contentNode[nc.timestampSimpleTextNode][nc.simpleTextNode]
        self.timeStamp = self.contentNode[nc.timestampUsecNode]
        self.author = self.contentNode[nc.authorNode][nc.simpleTextNode]
        self.contextMessage = self.extractMembershipContextMessage()

    def extractMembershipContextMessage(self):
        contextOutput = ''
        if(self.MESSAGE_TYPE == self.MESSAGE_TYPES["chatMessage"]):
            contextOutput = self.runsMessageBuilder(self.contentNode[nc.rendererNode][nc.messageNode][nc.runsNode])
        elif(self.MESSAGE_TYPE == self.MESSAGE_TYPES["joinMessage"]):
            contextOutput = self.runsMessageBuilder(self.contentNode[nc.rendererNode][nc.headerSubtextNode][nc.runsNode])
        else:
            contextOutput = "Unrecognized MESSAGE_TYPE"
        return contextOutput

    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage)