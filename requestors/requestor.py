from builders.continuationBuilder import ContinuationFetcher

class Requestor:
    BASE_URL = ''
    videoId = ''
    continuation = ''
    playerState = None
    fetcher = None
    response = None

    def __init__(self, videoId, playerState=None):
        self.videoId = videoId
        self.playerState = playerState

    def buildFetcher(self):
        self.fetcher = ContinuationFetcher(self.videoId, self.playerState)

    def updateFetcher(self, continuation, offset):
        self.fetcher.params["continuation"] = continuation
        self.fetcher.params["currentPlayerState"] = {"playerOffsetMs" : offset}