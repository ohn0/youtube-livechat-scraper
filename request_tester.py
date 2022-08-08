import pstats
import requests
from continuation_builder import ContinuationFetcher
from continuation_requestor import ContinuationRequestor
from livechat_requestor import livechatRequestor
from livechat_parser import livechatParser
from player_state import PlayerState
from subsequent_requestor import SubsequentRequestor
import json

session = requests.Session()
videoId = "N03T-jSJPvg"
# videoId = "ekzLANkyras"
expectedContinuation = "op2w0wRiGlhDaWtxSndvWVZVTkpaVk5WVkU5VWEwWTVTSE0zY1ROVFIyTlBMVTkzRWd0T01ETlVMV3BUU2xCMlp4b1Q2cWpkdVFFTkNndE9NRE5VTFdwVFNsQjJaeUFCQAFyAggEeAE%3D"
# expectedContinuation = "op2w0wRxGlhDaWtxSndvWVZVTm5RVEpxUzFKcmNYQlpYemhsZVhOUVZYTTRjMnAzRWd0bGEzcE1RVTVyZVhKaGN4b1Q2cWpkdVFFTkNndGxhM3BNUVU1cmVYSmhjeUFCKKGL7bwKQABIA1IFIACwAQByAggEeAA%3D"
pState = PlayerState()
pState.continuation = expectedContinuation

def continuationBuilderBuildsRequestCorrectlyAndGetsContinuation():
    url = "https://www.youtube.com/youtubei/v1/next?"
    continuationFetch = ContinuationFetcher(videoId)
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
    print(liveChatParser.initialContinuation)
    chatMessageList = []
    for c in content[1::]:
        chatMessageList.append(c["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]
                  ["liveChatTextMessageRenderer"]["message"]["runs"][0])
    return len(chatMessageList) > 0

def getSuccessfulSubsequentLiveChat(offset):
    pState.playerOffsetMs = offset
    requestor = SubsequentRequestor(videoId, pState)
    requestor.buildFetcher()
    requestor.makeRequest()
    return requestor.response

def printOffsets(offset):
    jsonContent = getSuccessfulSubsequentLiveChat(300000)
    for action in jsonContent["continuationContents"]["liveChatContinuation"]["actions"]:
        print(action["replayChatItemAction"]["videoOffsetTimeMsec"])



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

if not getSuccessfulSubsequentLiveChat(300000):
    print("call to get subsequent livechat requests failed")
else:
    print("Subsequent livechat caller good")
