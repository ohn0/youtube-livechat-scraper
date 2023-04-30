from messages.message import Message
from messages.fragments.content import Content
import constants.nodeConstants as nc
class membershipChatMessage(Message):
    membershipDurationHeader = ''
    MESSAGE_TYPES = {"chatMessage": "MEMBERSHIP_CHAT", 
                     "joinMessage" : "MEMBERSHIP_JOINED"}
    MESSAGE_TYPE_MEMBER_CHAT = "Membership Chat message"
    MESSAGE_TYPE_MEMBER_JOIN = "Membership Join message"
    MESSAGE_TYPE_MEMBER_RENEWAL = "Membership Renew message"
    MESSAGE_TYPE = None
    def __init__(self, chatAction):
        super().__init__(chatAction)
        self.CONTENT_NODE = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_MEMBERSHIP_NODE]

    def findMembershipMessageType(self):
        tooltip = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_MEMBERSHIP_NODE][nc.AUTHOR_BADGE_NODE][0][nc.LIVECHAT_AUTHOR_BADGE_NODE][nc.TOOLTIP_NODE]
        if(tooltip == "New member"):
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_JOIN
        elif(nc.MESSAGE_NODE in self.CONTENT_NODE):
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_CHAT
        else:
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_RENEWAL

    def buildMessage(self):
        self.findMembershipMessageType()
        self.occurrenceTimestamp = self.CONTENT_NODE[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        self.timeStamp = self.CONTENT_NODE[nc.TIMESTAMP_USEC_NODE]
        self.author = self.CONTENT_NODE[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.contextMessage = self.extractMembershipContextMessage()

    def extractMembershipContextMessage(self):
        contextOutput = ''
        if(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_CHAT):
            contextOutput = {"membershipChat" :  self.runsMessageBuilder(self.CONTENT_NODE[nc.MESSAGE_NODE][nc.RUNS_NODE])}
        elif(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_JOIN):
            contextOutput = {"membershipJoin" : self.runsMessageBuilder(self.CONTENT_NODE[nc.HEADER_SUBTEXT_NODE])}
        elif(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_RENEWAL):
            contextOutput = {"membershipRenewal" : self.runsMessageBuilder(self.CONTENT_NODE[nc.HEADER_SUBTEXT_NODE])}
        else:
            contextOutput = {"membershipError" : "Unrecognized MESSAGE_TYPE"}
        return contextOutput

    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage, self.MESSAGE_TYPE).objectOutput()