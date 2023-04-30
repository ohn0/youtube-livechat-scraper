from messages.fragments.content import Content

class Message:
    occurrenceTimestamp = None #time at which message was generated SINCE stream began
    timeStamp = None #time at which message was generated
    author = None
    outputMessage = ''
    action = None
    content_node = None
    contextMessage = None

    def __init__(self, action):
        self.action = action

    def buildMessage(self):
        pass

    def runsMessageBuilder(self, runs):
        builtMessage = ''
        for run in runs:
            if("text" in run):
                builtMessage = builtMessage + run["text"]
        return builtMessage

    def generateContent(self):
        pass