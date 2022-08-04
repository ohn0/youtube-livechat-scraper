import requests
from continuation_builder import ContinuationFetcher
from continuation_requestor import ContinuationRequestor
session = requests.Session()
videoId = "N03T-jSJPvg"
expectedContinuation = "op2w0wRiGlhDaWtxSndvWVZVTkpaVk5WVkU5VWEwWTVTSE0zY1ROVFIyTlBMVTkzRWd0T01ETlVMV3BUU2xCMlp4b1Q2cWpkdVFFTkNndE9NRE5VTFdwVFNsQjJaeUFCQAFyAggEeAE%3D"
def continuationBuilderBuildsRequestCorrectlyAndGetsContinuation():
    url = "https://www.youtube.com/youtubei/v1/next?"
    continuationFetch = ContinuationFetcher("N03T-jSJPvg")
    response = session.post(url, json=continuationFetch.params).json()
    continuation = response["contents"]["twoColumnWatchNextResults"]["conversationBar"]["liveChatRenderer"]["continuations"][0]["reloadContinuationData"]["continuation"]

    return continuation == expectedContinuation

def continuationRequestorMakesSuccessfulRequest():
    requestor = ContinuationRequestor(videoId)
    requestor.buildFetcher()
    requestor.makeRequest()
    return requestor.continuation == expectedContinuation

if not continuationBuilderBuildsRequestCorrectlyAndGetsContinuation():
    print("ContinuationFetcher testing failed. No value returned or returned value not matching expected value")
else:
    print("continuationFetcher good")

if not continuationRequestorMakesSuccessfulRequest():
    print("ContinuationRequestor failed to make a successful request to get continuation value")
else:
    print("ContinuationRequestor good")
