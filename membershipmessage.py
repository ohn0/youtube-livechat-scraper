from message import Message
from content import Content
import nodeConstants as nc
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
        self.contentNode = self.action[nc.addChatItemActionNode][nc.itemNode][nc.liveChatMembershipNode]

    def findMembershipMessageType(self):
        tooltip = self.action[nc.addChatItemActionNode][nc.itemNode][nc.liveChatMembershipNode][nc.authorBadgeNode][0][nc.livechatAuthorBadgeNode][nc.tooltipNode]
        if(tooltip == "New member"):
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_JOIN
        elif(nc.messageNode in self.contentNode):
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_CHAT
        else:
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_RENEWAL

    def buildMessage(self):
        self.findMembershipMessageType()
        self.occurrenceTimestamp = self.contentNode[nc.timestampSimpleTextNode][nc.simpleTextNode]
        self.timeStamp = self.contentNode[nc.timestampUsecNode]
        self.author = self.contentNode[nc.authorNode][nc.simpleTextNode]
        self.contextMessage = self.extractMembershipContextMessage()

    def extractMembershipContextMessage(self):
        contextOutput = ''
        if(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_CHAT):
            contextOutput = {"membershipChat" :  self.runsMessageBuilder(self.contentNode[nc.messageNode][nc.runsNode])}
        elif(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_JOIN):
            contextOutput = {"membershipJoin" : self.runsMessageBuilder(self.contentNode[nc.headerSubtextNode])}
        elif(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_RENEWAL):
            contextOutput = {"membershipRenewal" : self.runsMessageBuilder(self.contentNode[nc.headerSubtextNode])}
        else:
            contextOutput = {"membershipError" : "Unrecognized MESSAGE_TYPE"}
        return contextOutput

    def generateContent(self):
        return Content(self.occurrenceTimestamp, self.timeStamp, self.author, self.contextMessage, self.MESSAGE_TYPE).objectOutput()