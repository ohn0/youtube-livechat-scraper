import requests
from continuation_builder import ContinuationFetcher
from requestor import Requestor
class SubsequentRequestor(Requestor):
    def __init__(self):
        self.BASE_URL = 'https://www.youtube.com/youtubei/v1/live_chat/get_live_chat_replay?prettyPrint=false'


    
    