import re
from wsgiref.util import request_uri
from requests import Session
import json

class livechatRequestor:
    continuation = ''
    REPLAY_URL = "https://www.youtube.com/live_chat_replay?continuation="
    request_url = ""
    initialLiveChat = ""
    def __init__(self, continuation):
        self.continuation = continuation

    def buildURL(self):
        self.request_url = self.REPLAY_URL + self.continuation
        
    def getLiveChatData(self):
        with Session() as session:
            self.initialLiveChat = session.get(self.request_url)
        return self.initialLiveChat

            