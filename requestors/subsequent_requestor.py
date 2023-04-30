"""handles making consecutive requests for livechat data and \
    updates with the next continuation value to grab the next request"""
import json
import time

import requests

import constants.scraper_constants as c
from requestors.requestor import Requestor


class SubsequentRequestor(Requestor):
    """makes consecutive requests through make_request, """
    debug_output_name = "output/subsequentContents_"
    def __init__(self, videoId, pState):
        super().__init__(videoId, pState)
        self.base_url = \
            'https://www.youtube.com/youtubei/v1/live_chat/get_live_chat_replay?prettyPrint=false'
        self.continuation = self.player_state.continuation

    def make_request(self, debug = False):
        """makes a POST call to youtube, with a configured params\
             object to fetch the next batch of messages"""
        with requests.Session() as session:
            self.response = session.post(self.base_url, json=self.fetcher.params).json()
        if debug:
            with open(f'{self.debug_output_name}{time.time()}.json', \
                'w', encoding='utf-8') as writer:
                json.dump(self.response, writer)
                json.dump(self.fetcher.params, writer)

    def update_continuation(self, response):
        """updates the continuation value with the update value from \
            the response to be used in the next make_request."""
        if "liveChatReplayContinuationData" in \
            response["continuationContents"]["liveChatContinuation"]["continuations"][0]:
            self.continuation =response["continuationContents"]["liveChatContinuation"]\
                ["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
        else:
            self.continuation = c.SCRAPE_FINISHED
        return self.continuation
