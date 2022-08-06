import requests
from continuation_builder import ContinuationFetcher
from requestor import Requestor

class ContinuationRequestor(Requestor):
    videoId = ""
    fetcher = None
    response = None
    continuation = None
    playerState = None

    def __init__(self, videoId):
        self.videoId = videoId
        self.BASE_URL = 'https://www.youtube.com/youtubei/v1/next?'
    def buildFetcher(self):
        self.fetcher = ContinuationFetcher(self.videoId, self.playerState)

    def makeRequest(self):
        with requests.Session() as continuationFetchSession:
            self.response = continuationFetchSession.post(self.BASE_URL, json=self.fetcher.params).json()
        self.bindContinuation()    
        
    def bindContinuation(self):
        self.continuation = self.response["contents"]["twoColumnWatchNextResults"]["conversationBar"]["liveChatRenderer"]["continuations"][0]["reloadContinuationData"]["continuation"]

    def updatePlayerState(self, playerState):
        self.playerState = playerState