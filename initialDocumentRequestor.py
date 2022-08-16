from requestor import Requestor
import requests
class initialDocumentRequestor(Requestor):
    response = ''
    def __init__(self):
        super().__init__(None, None)

    def getContent(self, url):
        with requests.Session() as session:
            self.response = session.get(url)
        return self.response
    