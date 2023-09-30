"""Message output for membership chat and membership join messages sent in livechat"""
from livechat_scraper.messages.message import Message
from livechat_scraper.messages.fragments.content import Content
import livechat_scraper.constants.node_constants as nc
class MembershipChatMessage(Message):
    """Message output for membership chat and membership join messages sent in livechat"""
    membershipDurationHeader = ''
    MESSAGE_TYPES = {"chat_message": "MEMBERSHIP_CHAT", 
                     "joinMessage" : "MEMBERSHIP_JOINED"}
    MESSAGE_TYPE_MEMBER_CHAT = "Membership Chat message"
    MESSAGE_TYPE_MEMBER_JOIN = "Membership Join message"
    MESSAGE_TYPE_MEMBER_RENEWAL = "Membership Renew message"
    message_type = None
    def __init__(self, chatAction):
        super().__init__(chatAction)
        self.content_node = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE]\
            [nc.LIVECHAT_MEMBERSHIP_NODE]

    def __find_membership_message_type(self):
        tooltip = self.action[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE]\
            [nc.LIVECHAT_MEMBERSHIP_NODE][nc.AUTHOR_BADGE_NODE][0]\
                [nc.LIVECHAT_AUTHOR_BADGE_NODE][nc.TOOLTIP_NODE]
        if tooltip == "New member":
            self.message_type = self.MESSAGE_TYPE_MEMBER_JOIN
        elif nc.MESSAGE_NODE in self.content_node:
            self.message_type = self.MESSAGE_TYPE_MEMBER_CHAT
        else:
            self.message_type = self.MESSAGE_TYPE_MEMBER_RENEWAL

    def build_message(self):
        """builds the membership joined/chat message object for scraper
        consumption, along with bringing over metadata."""
        self.__find_membership_message_type()
        self.occurrence_timestamp = self.content_node\
            [nc.TIMESTAMP_SIMPLE_TEXT_NODE][nc.SIMPLE_TEXT_NODE]
        self.time_stamp = self.content_node[nc.TIMESTAMP_USEC_NODE]
        self.author = self.content_node[nc.AUTHOR_NODE][nc.SIMPLE_TEXT_NODE]
        self.context_message = self.__extract_membership_context_message()

    def __extract_membership_context_message(self):
        context_output = ''
        if self.message_type == self.MESSAGE_TYPE_MEMBER_CHAT:
            context_output = {"membershipChat" :  \
                self.runs_message_builder(self.content_node[nc.MESSAGE_NODE][nc.RUNS_NODE])}
        elif self.message_type == self.MESSAGE_TYPE_MEMBER_JOIN:
            context_output = {"membershipJoin" : \
                self.runs_message_builder(self.content_node[nc.HEADER_SUBTEXT_NODE])}
        elif self.message_type == self.MESSAGE_TYPE_MEMBER_RENEWAL:
            context_output = {"membershipRenewal" : \
                self.runs_message_builder(self.content_node[nc.HEADER_SUBTEXT_NODE])}
        else:
            context_output = {"membershipError" : "Unrecognized MESSAGE_TYPE"}
        return context_output

    def generate_content(self):
        """returns object for output consumption"""
        return Content(self.occurrence_timestamp, self.time_stamp, \
            self.author, self.context_message, self.message_type).object_output()
            