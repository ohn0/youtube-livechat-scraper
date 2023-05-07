"""Module for first livechat request."""
import requests

from requestors.requestor import Requestor


class InitialDocumentRequestor(Requestor):
    """Initial livechat request class, which makes the first request to start the
    scraping process, the first request differs from all the subsequent
    requests as the initial livechat data is returned in an HTML file along
    with the livechat object DOM."""
    response = ''
    def __init__(self):
        super().__init__(None, None)

    def get_content(self, url):
        """makes a request for the initial livechat data and returns
        a successful response."""
        with requests.Session() as session:
            self.response = session.get(url)
        return self.response
    