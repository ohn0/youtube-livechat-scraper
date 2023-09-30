"""module for getting each subsequent livechat request"""

from requests import Session


class LivechatRequestor:
    """Class for making each subsequent livechat request call to Youtube
    to perform scraping."""
    continuation = ''
    REPLAY_URL = "https://www.youtube.com/live_chat_replay?continuation="
    request_url = ""
    livechat = ""
    headers = {
        'User-Agent' : \
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }
    def __init__(self, continuation):
        self.continuation = continuation
        self.request_url = self.REPLAY_URL + self.continuation

    def get_livechat_data(self):
        """make requests to Youtube to fetch livechat data fragments"""
        with Session() as session:
            self.livechat = session.get(self.request_url, headers=self.headers)
        return self.livechat
