"""definitions for how the Content is generated and is output is stored in the Content class"""
class Content:
    """Content class that defines the output fields for each message scraped"""
    def __init__(self, occurence_timestamp, timestamp, author, content, message_type):
        self.occurence_timestamp = occurence_timestamp
        self.timestamp = timestamp
        self.author = author
        self.content = content
        self.message_type = message_type

    def simple_output(self):
        """returns simple output that is message's occurrence time, author, and content generated"""
        return f"{self.occurence_timestamp} : {self.author} : {self.content}"

    def object_output(self):
        """returns an object that generates a JSON output for each message."""
        return {
            "message_type" : self.message_type,
            "occurence_timestamp" : self.occurence_timestamp,
            "timeStampUTC" : self.timestamp,
            "author" : self.author,
            "content" : self.content
        }
        