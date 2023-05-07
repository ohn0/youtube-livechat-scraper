from extractors.initial_document_extractor import InitialExtractor
from parsers.livechatParser import livechatParser
from requestors.continuation_requestor import ContinuationRequestor
from requestors.initialDocumentRequestor import initialDocumentRequestor
from requestors.livechatRequestor import livechatRequestor


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
        parser = livechatParser('html.parser')
        parser.buildParser(initialContents)
        parser.findContent()
        return parser.initialContinuation

    def generateInitialContent(self, videoUrl):
        documentRequestor = initialDocumentRequestor()
        return InitialExtractor().build_and_get_script(documentRequestor.get_content(videoUrl).text)
