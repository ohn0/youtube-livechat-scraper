from continuationRequestor import ContinuationRequestor
from livechatRequestor import livechatRequestor
from livechatParser import livechatParser
from initialDocumentRequestor import initialDocumentRequestor
from initialDocumentExtractor import initialExtractor
class ScraperInitializer:
    def __init__(self) -> None:
        pass

    def generateInitialState(self, videoId):
        requestor = ContinuationRequestor(videoId)
        requestor.buildFetcher()
        requestor.makeRequest()
        return self.generateInitialContinuation(requestor.continuation)

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
        return initialExtractor().buildAndGetScript(documentRequestor.getContent(videoUrl).text)
