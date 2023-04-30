"""holds a video and the current state of the stream; where the scrape is currently scraping."""
from builders.continuationBuilder import ContinuationFetcher

class Requestor:
    """holds a livestream archive and the currently scraped location along the stream's timeline."""
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
        """Creates a continuation fetcher to grab the next request."""
        self.fetcher = ContinuationFetcher(self.video_id, self.player_state)

    def update_fetcher(self, continuation, offset):
        """Updates the fetcher to point to the next continuation value and time"""
        self.fetcher.params["continuation"] = continuation
        self.fetcher.params["currentPlayerState"] = {"playerOffsetMs" : offset}
