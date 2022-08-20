from content import Content

class Message:
    occurrenceTimestamp = None #time at which message was generated SINCE stream began
    timeStamp = None #time at which message was generated
    author = None
    outputMessage = ''
    action = None
    contentNode = None
    contextMessage = None

    def __init__(self, action):
        self.action = action

    def buildMessage(self):
        pass

    def runsMessageBuilder(self, runs):
        builtMessage = ''
        for run in runs[0]:
            builtMessage += run["text"]
        
        return builtMessage

    def generateContent(self):
        pass