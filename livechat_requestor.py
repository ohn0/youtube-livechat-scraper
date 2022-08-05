import re
from wsgiref.util import request_uri
from requests import Session
import json

class livechatRequestor:
    continuation = ''
    REPLAY_URL = "https://www.youtube.com/live_chat_replay?continuation="
    request_url = ""
    initialLiveChat = ""
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }
    def __init__(self, continuation):
        self.continuation = continuation

    def buildURL(self):
        self.request_url = self.REPLAY_URL + self.continuation
        
    def getLiveChatData(self):
        with Session() as session:
            self.initialLiveChat = session.get(self.request_url, headers=self.headers)
        return self.initialLiveChat

            