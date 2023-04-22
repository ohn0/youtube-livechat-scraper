import requests
from builders.continuationBuilder import ContinuationFetcher
from requestors.requestor import Requestor
import constants.nodeConstants
import json

class ContinuationRequestor(Requestor):

    def __init__(self, videoId):
        super().__init__(videoId)
        self.BASE_URL = 'https://www.youtube.com/youtubei/v1/next?'

    def makeRequest(self):
        with requests.Session() as continuationFetchSession:
            self.response = continuationFetchSession.post(self.BASE_URL, json=self.fetcher.params).json()
        self.bindContinuation()    
        
    def bindContinuation(self):
        try:
            self.continuation = self.response[constants.nodeConstants.contentNode][constants.nodeConstants.twoColumnWatchNextResultsNode] \
            [constants.nodeConstants.conversationBarNode][constants.nodeConstants.liveChatRendererNode][constants.nodeConstants.continuationsNode] \
            [0][constants.nodeConstants.reloadContinuationDataNode][constants.nodeConstants.continuationNode]
        except KeyError:
            print("Unable to find matching key, video stream might not have a livechat or livechat could still be processing.")
            