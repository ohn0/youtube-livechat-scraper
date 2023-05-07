from messages.message import Message
from messages.fragments.content import Content
import constants.node_constants as nc
class MembershipChatMessage(Message):
    membershipDurationHeader = ''
    MESSAGE_TYPES = {"chat_message": "MEMBERSHIP_CHAT", 
                     "joinMessage" : "MEMBERSHIP_JOINED"}
    MESSAGE_TYPE_MEMBER_CHAT = "Membership Chat message"
    MESSAGE_TYPE_MEMBER_JOIN = "Membership Join message"
    MESSAGE_TYPE_MEMBER_RENEWAL = "Membership Renew message"
    MESSAGE_TYPE = None
    def __init__(self, chatAction):
        super().__init__(chatAction)
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_MEMBERSHIP_NODE]

    def findMembershipMessageType(self):
        tooltip = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE][nc.LIVECHAT_MEMBERSHIP_NODE][nc.AUTHOR_BADGE_NODE][0][nc.LIVECHAT_AUTHOR_BADGE_NODE][nc.TOOLTIP_NODE]
        if(tooltip == "New member"):
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_JOIN
        elif(nc.MESSAGE_NODE in self.content_node):
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_CHAT
        else:
            self.MESSAGE_TYPE = self.MESSAGE_TYPE_MEMBER_RENEWAL

    def build_message(self):
        self.findMembershipMessageType()
        self.occurrence_timestamp = self.content_node[nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        self.time_stamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        self.author = self.content_node[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.context_message = self.extractMembershipContextMessage()

    def extractMembershipContextMessage(self):
        contextOutput = ''
        if(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_CHAT):
            contextOutput = {"membershipChat" :  self.runs_message_builder(self.content_node[nc.MESSAGE_NODE][nc.RUNS_NODE])}
        elif(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_JOIN):
            contextOutput = {"membershipJoin" : self.runs_message_builder(self.content_node[nc.HEADER_SUBTEXT_NODE])}
        elif(self.MESSAGE_TYPE == self.MESSAGE_TYPE_MEMBER_RENEWAL):
            contextOutput = {"membershipRenewal" : self.runs_message_builder(self.content_node[nc.HEADER_SUBTEXT_NODE])}
        else:
            contextOutput = {"membershipError" : "Unrecognized MESSAGE_TYPE"}
        return contextOutput

    def generate_content(self):
        return Content(self.occurrence_timestamp, self.time_stamp, self.author, self.context_message, self.MESSAGE_TYPE).object_output()