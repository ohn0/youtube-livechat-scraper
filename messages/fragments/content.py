class Content:
    occurrenceTimestamp = None
    timeStamp = None
    author = None
    content = None
    messageType = None
    
    def __init__(self, occurrenceTimeStamp, timeStamp, author, content, messageType):
        self.OCCURENCE_TIMESTAMP = occurrenceTimeStamp
        self.timeStamp = timeStamp
        self.AUTHOR = author
        self.CONTENT = content
        self.messageType = messageType

    def simpleOutput(self):
        return f"{self.OCCURENCE_TIMESTAMP} : {self.AUTHOR} : {self.CONTENT}"

    def objectOutput(self):
        return {
            "messageType" : self.messageType,
            "occurrenceTimestamp" : self.OCCURENCE_TIMESTAMP,
            "timeStampUTC" : self.timeStamp,
            "author" : self.AUTHOR,
            "content" : self.CONTENT
        }