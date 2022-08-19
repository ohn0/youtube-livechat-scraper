from message import Message

class membershipChatMessage(Message):
    membershipDurationHeader = ''
    MESSAGE_TYPES = {"chatMessage": "MEMBERSHIP_CHAT", 
                     "joinMessage" : "MEMBERSHIP_JOINED"}
    MESSAGE_TYPE = None
    def __init__(self, chatAction):
        super().__init__(chatAction)

    def findMembershipMessageType(self):
        if(self.accessibilityNode in self.action[self.tickerItemActionNode][self.itemNode][self.liveChatTickerSponsorNode][self.detailTextNode]):
            self.MESSAGE_TYPE = self.MESSAGE_TYPES["chatMessage"]
        elif(self.runsNode in self.action[self.tickerItemActionNode][self.itemNode][self.liveChatTickerSponsorNode][self.detailTextNode]):
            self.MESSAGE_TYPE = self.MESSAGE_TYPES["joinMessage"]

    def extractContents(self):
        self.contentNode = self.action[self.tickerItemActionNode][self.itemNode][self.liveChatTickerSponsorNode]
        self.occurrenceTimestamp = self.contentNode[self.showItemEndpointNode][self.showLiveChatEndpointNode][self.liveChatMembershipNode][self.timestampSimpleTextNode][self.simpleTextNode]
        self.timeStamp = self.contentNode[self.showItemEndpointNode][self.showLiveChatEndpointNode][self.liveChatMembershipNode][self.timestampUsecNode]
        self.author = self.contentNode[self.showItemEndpointNode][self.showLiveChatEndpointNode][self.liveChatMembershipNode][self.authorNode][self.simpleTextNode]
        membershipContextMessage = self.extractMembershipContextMessage()
        self.outputMessage = 

    def extractMembershipContextMessage(self):
        contextOutput = ''
        if(self.MESSAGE_TYPE == self.MESSAGE_TYPES["chatMessage"]):
            contextOutput = self.runsMessageBuilder(self.contentNode[self.showItemEndpointNode][self.showLiveChatEndpointNode][self.rendererNode][self.liveChatMembershipNode][self.messageNode][self.runsNode])
        elif(self.MESSAGE_TYPE == self.MESSAGE_TYPES["joinMessage"]):
            contextOutput = self.runsMessageBuilder(self.contentNode[self.showItemEndpointNode][self.showLiveChatEndpointNode][self.rendererNode][self.liveChatMembershipNode][self.headerSubtextNode][self.runsNode])
        else:
            contextOutput = "Unrecognized MESSAGE_TYPE"
        return contextOutput