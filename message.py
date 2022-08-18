from sqlite3 import Timestamp


class Message:
    occurrenceTimestamp = None #time at which message was generated SINCE stream began
    timeStamp = None #time at which message was generated
    author = None
    outputMessage = ''
    def __init__(self):
        pass

    def buildMessage(self):
        pass

    def runsMessageBuilder(self, runs):
        builtMessage = ''
        for run in runs[0]:
            builtMessage += run["text"]
        
        return builtMessage