import requests

import constants.node_constants
from requestors.requestor import Requestor


class ContinuationRequestor(Requestor):

    def __init__(self, videoId):
        super().__init__(videoId)
        self.base_url = 'https://www.youtube.com/youtubei/v1/next?'

    def make_request(self):
        """makes a request to youtube to fetch next batch of livechat messages"""
        with requests.Session() as continuation_fetch_session:
            self.response = continuation_fetch_session.post(self.base_url, \
                json=self.fetcher.params).json()
        self.__bind_continuation()

    def __bind_continuation(self):
        try:
            self.continuation = self.response[constants.node_constants.CONTENT_NODE]\
            [constants.node_constants.TWO_COLUMN_WATCH_NEXT_RESULTS_NODE][constants.node_constants\
            .CONVERSATION_BAR_NODE][constants.node_constants.LIVECHAT_RENDERER_NODE][constants.\
            node_constants.CONTINUATIONS_NODE][0][constants.node_constants.\
            RELOAD_CONTINUATION_DATA_NODE][constants.node_constants.CONTINUATION_NODE]
        except KeyError:
            print("Unable to find matching key, video stream might not have a livechat \
                or livechat could still be processing.")
            