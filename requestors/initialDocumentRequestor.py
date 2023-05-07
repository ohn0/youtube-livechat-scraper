import requests

from requestors.requestor import Requestor


class initialDocumentRequestor(Requestor):
    response = ''
    def __init__(self):
        super().__init__(None, None)

    def get_content(self, url):
        with requests.Session() as session:
            self.response = session.get(url)
        return self.response
    