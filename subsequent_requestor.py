import requests
from continuation_builder import ContinuationFetcher
from requestor import Requestor
from player_state import PlayerState
class SubsequentRequestor(Requestor):
    def __init__(self, videoId, pState):
        super().__init__(videoId, pState)
        self.BASE_URL = 'https://www.youtube.com/youtubei/v1/live_chat/get_live_chat_replay?prettyPrint=false'
        self.continuation = self.playerState.continuation

    def makeRequest(self):
        print(self.fetcher.params)
        with requests.Session() as session:
            self.response = session.post(self.BASE_URL, json=self.fetcher.params).json()
        