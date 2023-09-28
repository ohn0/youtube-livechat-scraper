"""Base module for all generated messages."""
class Message:
    """Base message class for all types of scraped messages"""
    def __init__(self, action):
        self.occurrence_timestamp = None #time at which message was generated SINCE stream began
        self.time_stamp = None #time at which message was generated
        self.author = None
        self.outputMessage = ''
        self.action = None
        self.content_node = None
        self.context_message = None
        self.action = action

    def runs_message_builder(self, runs):
        """constructs a full message given a set of runs which contain YT scraped data"""
        build_message = ''
        for run in runs:
            if "text" in run:
                build_message = build_message + run["text"]
        return build_message
        