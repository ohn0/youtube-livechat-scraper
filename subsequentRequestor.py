import requests
from continuationBuilder import ContinuationFetcher
from requestor import Requestor
from playerState import PlayerState
import json
import time
import constants as c
class SubsequentRequestor(Requestor):
    def __init__(self, videoId, pState):
        super().__init__(videoId, pState)
        self.BASE_URL = 'https://www.youtube.com/youtubei/v1/live_chat/get_live_chat_replay?prettyPrint=false'
        self.continuation = self.playerState.continuation

    def makeRequest(self, debug = False):
        with requests.Session() as session:
            self.response = session.post(self.BASE_URL, json=self.fetcher.params).json()
        if(debug):
            with open('output/subsequentContents_{0}.json'.format(time.time()), 'w', encoding='utf-8') as writer:
                json.dump(self.response, writer)
                json.dump(self.fetcher.params, writer)

    def updateContinuation(self, response):
        if("liveChatReplayContinuationData" in response["continuationContents"]["liveChatContinuation"]["continuations"][0]):
            self.continuation = response["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
        else:
            self.continuation = c.SCRAPE_FINISHED
        return self.continuation