from extractors.initial_document_extractor import InitialExtractor
from parsers.livechat_parser import LivechatParser
from requestors.continuation_requestor import ContinuationRequestor
from requestors.initial_document_requestor import initialDocumentRequestor
from requestors.livechat_requestor import livechatRequestor


class ScraperInitializer:
    def __init__(self) -> None:
        pass

    def generateInitialState(self, video_id):
        try:
            requestor = ContinuationRequestor(video_id)
            requestor.build_fetcher()
            requestor.make_request()
            return self.generateInitialContinuation(requestor.continuation)
        except Exception as _:
            print("error configuring initial scraper state and making first request")

    def generateInitialContinuation(self, continuation):
        contents = livechatRequestor(continuation)
        contents.buildURL()
        initialContents = contents.getLiveChatData()
        parser = LivechatParser('html.parser')
        parser.build_parser(initialContents)
        parser.find_content()
        return parser.initial_continuation

    def generateInitialContent(self, videoUrl):
        documentRequestor = initialDocumentRequestor()
        return InitialExtractor().build_and_get_script(documentRequestor.get_content(videoUrl).text)
