"""Module for initializing scraper and setting up the initial state and making the first
request."""
from livechat_scraper.extractors.initial_document_extractor import InitialExtractor
from livechat_scraper.parsers.livechat_parser import LivechatParser
from livechat_scraper.requestors.continuation_requestor import ContinuationRequestor
from livechat_scraper.requestors.initial_document_requestor import InitialDocumentRequestor
from livechat_scraper.requestors.livechat_requestor import LivechatRequestor


class ScraperInitializer:
    """Class for initializing scraper, setting up the initial state and getting the first
    continuation value from youtube."""
    def __init__(self) -> None:
        pass

    def generate_initial_state(self, video_id):
        """Make initial request for first continuatioan value, then use the continuation
        value to fetch livechat data and return parsed data."""
        try:
            requestor = ContinuationRequestor(video_id)
            requestor.build_fetcher()
            requestor.make_request()
            return self.__generate_initial_livechat(requestor.continuation)
        except Exception as _:
            print("error configuring initial scraper state and making first request")

    def __generate_initial_livechat(self, continuation):
        contents = LivechatRequestor(continuation)
        initial_contents = contents.get_livechat_data()
        parser = LivechatParser('html.parser')
        parser.build_parser(initial_contents)
        parser.find_content()
        return parser.initial_continuation

    def generate_initial_content(self, video_url):
        """Get the initial HTML script that will contain the first continuation value."""
        requestor = InitialDocumentRequestor()
        return InitialExtractor().build_and_get_script(requestor.get_content(video_url).text)
