from message import Message
from emoji import Emoji
import nodeConstants as nc

class chatMessage(Message):
    def __init__(self, action):
        super().__init__(action)

    def buildMessage(self):
        self.occurrenceTimestamp = self.action[nc.replayActionNode][nc.videoOffsetTimeMsecNode]
        self.contentNode = self.action[nc.replayActionNode][nc.actionsNode][0][nc.addChatItemActionNode][nc.itemNode][nc.liveChatTextMessageRendererNode]
        self.timeStamp = self.contentNode[nc.timestampSimpleTextNode][nc.simpleTextNode]
        self.author = self.contentNode[nc.authorNode][nc.simpleTextNode]
        self.contextMessage = {
            "message" : self.contentNode[nc.messageNode][nc.runsNode][0][nc.textNode],
            "emoji" : self.extractEmojis([self.contentNode][nc.messageNode][nc.runsNode][0]) 
        }

    def extractEmojis(self, runs):
        emojis = []
        for run in runs:
            if("emoji" in run):
                emojis.append(Emoji(run["emoji"]))
        
        return emojis
