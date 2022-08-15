import requests
from continuation_builder import ContinuationFetcher
from requestor import Requestor
import json

class ContinuationRequestor(Requestor):

    def __init__(self, videoId):
        super().__init__(videoId)
        self.BASE_URL = 'https://www.youtube.com/youtubei/v1/next?'

    def makeRequest(self):
        with requests.Session() as continuationFetchSession:
            self.response = continuationFetchSession.post(self.BASE_URL, json=self.fetcher.params).json()
        # with open('continuationContentsRequest.json', 'w', encoding='utf-8') as writer:
        #     json.dump(self.fetcher.params, writer)
                
        # with open('continuationContents.json', 'w', encoding='utf-8') as writer:
        #     json.dump(self.response, writer)
        self.bindContinuation()    
        
    def bindContinuation(self):
        self.continuation = self.response["contents"]["twoColumnWatchNextResults"]["conversationBar"]["liveChatRenderer"]["continuations"][0]["reloadContinuationData"]["continuation"]
