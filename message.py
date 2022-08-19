from sqlite3 import Timestamp


class Message:
    occurrenceTimestamp = None #time at which message was generated SINCE stream began
    timeStamp = None #time at which message was generated
    author = None
    outputMessage = ''
    action = None
    contentNode = None
    tickerItemActionNode = "addLiveChatTickerItemAction"
    itemNode = "item"
    liveChatTickerSponsorNode = "liveChatTickerSponsorItemRenderer"
    detailTextNode = "detailText"
    accessibilityNode = "accessibilityData"
    showItemEndpointNode = "showItemEndpoint"
    showLiveChatEndpointNode = "showLiveChatItemEndpoint"
    rendererNode = "renderer"
    liveChatMembershipNode = "liveChatMembershipItemRenderer"
    timestampUsecNode = "timestampUsec"
    timestampSimpleTextNode = "timestampText"
    simpleTextNode = "simpleText"
    authorNode = "authorName"
    messageNode = "message"
    headerSubtextNode = "headerSubtext"
    runsNode = "runs"

    def __init__(self, action):
        self.action = action

    def buildMessage(self):
        pass

    def runsMessageBuilder(self, runs):
        builtMessage = ''
        for run in runs[0]:
            builtMessage += run["text"]
        
        return builtMessage

    def extractContents(self):
        pass