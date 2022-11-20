class Content:
    occurrenceTimestamp = None
    timeStamp = None
    author = None
    content = None
    messageType = None
    
    def __init__(self):
        pass

    def __init__(self, occurrenceTimeStamp, timeStamp, author, content, messageType):
        self.occurrenceTimestamp = occurrenceTimeStamp
        self.timeStamp = timeStamp
        self.author = author
        self.content = content
        self.messageType = messageType

    def simpleOutput(self):
        return f"{self.occurrenceTimestamp} : {self.author} : {self.content}"

    def objectOutput(self):
        return {
            "messageType" : self.messageType,
            "occurrenceTimestamp" : self.occurrenceTimestamp,
            "timeStampUTC" : self.timeStamp,
            "author" : self.author,
            "content" : self.content
        }