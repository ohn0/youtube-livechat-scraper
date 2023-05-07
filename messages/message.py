"""Base module for all generated messages."""
class Message:
    """Base message class for all types of scraped messages"""
    occurrence_timestamp = None #time at which message was generated SINCE stream began
    time_stamp = None #time at which message was generated
    author = None
    outputMessage = ''
    action = None
    content_node = None
    context_message = None

    def __init__(self, action):
        self.action = action

    def runs_message_builder(self, runs):
        """constructs a full message given a set of runs which contain YT scraped data"""
        build_message = ''
        for run in runs:
            if "text" in run:
                build_message = build_message + run["text"]
        return build_message
        