class Content:
    occurrenceTimestamp = None
    timeStamp = None
    author = None
    content = ''
    
    def __init__(self):
        pass

    def __init__(self, occurrenceTimeStamp, timeStamp, author, content):
        self.occurrenceTimestamp = occurrenceTimeStamp
        self.timeStamp = timeStamp
        self.author = author
        self.content = content

    def simpleOutput(self):
        return f"{self.occurrenceTimestamp} : {self.author} : {self.content}"

    def objectOutput(self):
        return {
            "occurrenceTimestamp" : self.occurrenceTimestamp,
            "timeStampUTC" : self.timeStamp,
            "author" : self.author,
            "content" : self.content
        }