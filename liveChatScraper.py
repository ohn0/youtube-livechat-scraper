import requests
from continuation_builder import ContinuationFetcher
from continuation_requestor import ContinuationRequestor
from livechat_requestor import livechatRequestor
from livechat_parser import livechatParser
from player_state import PlayerState
from subsequent_requestor import SubsequentRequestor

class LiveChatScraper:
    videoId = None
    def __init__(self, videoUrl):
        #TODO save videoID from URL
        return

    def extractVideoID(self, videoUrl):
        #TODO pull out video ID
        return 

    '''
        step 1: 
            Grab initial continuation value  using continuation builder and requestors, these will require the videoId
        
        step 2:
            Use initial continuation value to fetch first livechat request using livechat_requestor and livechat_parser.
            The first livechat contents will be returned in a script embedded in a HTML document, which is why the parser is required
            to extract the contents.

            Ensure the continuation value updates after the livechat_requestor is done executing. The continuation value will update 
            each time a request is made as it is used to keep track of where we are on the video's timeline.

        step 3:
            Use subsequent_requestor and start a loop to grab each block of livechat data. Each time a request is made, the continuation
            value MUST be update to ensure the next obtained block of data does not contain any duplicates or missed values.
    '''