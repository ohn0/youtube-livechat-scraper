from builders.continuationBuilder import ContinuationFetcher

class Requestor:
    base_url = ''
    video_id = ''
    continuation = ''
    player_state = None
    fetcher = None
    response = None

    def __init__(self, video_id, player_state=None):
        self.video_id = video_id
        self.player_state = player_state

    def build_fetcher(self):
        self.fetcher = ContinuationFetcher(self.video_id, self.player_state)

    def update_fetcher(self, continuation, offset):
        self.fetcher.params["continuation"] = continuation
        self.fetcher.params["currentPlayerState"] = {"playerOffsetMs" : offset}
