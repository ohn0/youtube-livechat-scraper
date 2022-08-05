import requests
from continuation_builder import ContinuationFetcher
from continuation_requestor import ContinuationRequestor
from livechat_requestor import livechatRequestor
from livechat_parser import livechatParser

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

def getSuccessfulInitialLiveChat():
    requestor = ContinuationRequestor(videoId)
    requestor.buildFetcher()
    requestor.makeRequest()

    liveChatRequestor = livechatRequestor(requestor.continuation)
    liveChatRequestor.buildURL()
    initialLiveChatData = liveChatRequestor.getLiveChatData()

    liveChatParser = livechatParser('html.parser')
    liveChatParser.buildParser(initialLiveChatData)
    content = liveChatParser.findContent()
    chatMessageList = []
    for c in content[1::]:
        chatMessageList.append(c["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]
                  ["liveChatTextMessageRenderer"]["message"]["runs"][0])
    return len(chatMessageList) > 0


if not continuationBuilderBuildsRequestCorrectlyAndGetsContinuation():
    print("ContinuationFetcher testing failed. No value returned or returned value not matching expected value")
else:
    print("continuationFetcher good")

if not continuationRequestorMakesSuccessfulRequest():
    print("ContinuationRequestor failed to make a successful request to get continuation value")
else:
    print("ContinuationRequestor good")

if not getSuccessfulInitialLiveChat():
    print("Unable to make a successful initial livechat request to youtube and successfully parse data")
else:
    print("Calling initial live chat and parsing response good")
