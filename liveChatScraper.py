import nodeConstants as nc
from continuation_requestor import ContinuationRequestor
from livechat_requestor import livechatRequestor
from livechat_parser import livechatParser
from player_state import PlayerState
from subsequent_requestor import SubsequentRequestor
from initialDocumentExtractor import initialExtractor
from initialDocumentRequestor import initialDocumentRequestor
from PinnedMessage import PinnedMessage
from superchatMessage import superchatMessage
from membershipmessage import membershipChatMessage
from membershipGiftedMessage import membershipGiftedMessage
from chatMessage import chatMessage
import json
import time

CONTINUATION_FETCH_BASE_URL = "https://www.youtube.com/youtubei/v1/next?"

class LiveChatScraper:
    videoId = None
    videoUrl = None
    continuation = ''
    playerState = None
    contentSet = []
    content = ''
    currentOffsetTimeMsec = 0
    initialLiveChatContents = None
    endTime = 0
    VIDEO_ID_LENGTH = 11

    def __init__(self, videoUrl):
        self.videoUrl= videoUrl
        self.extractVideoID(videoUrl)

    def getEndTime(self):
        documentRequestor = initialDocumentRequestor()
        initialDocument = documentRequestor.getContent(self.videoUrl)
        endTimeSeeker = initialExtractor()
        initialContent = endTimeSeeker.buildAndGetScript(initialDocument.text)
        return initialContent["streamingData"]["formats"][0]["approxDurationMs"]

    def extractVideoID(self, videoUrl):
        keyStart = videoUrl.find('=')+1
        keyEnd = keyStart + self.VIDEO_ID_LENGTH
        self.videoId = videoUrl[keyStart:keyEnd]

    def getContinuation(self):
        continuationRequestor = ContinuationRequestor(self.videoId)
        continuationRequestor.buildFetcher()
        continuationRequestor.makeRequest()

        self.continuation = continuationRequestor.continuation

    def getInitialLiveChatContents(self):
        liveChatContents = livechatRequestor(self.continuation)
        liveChatContents.buildURL()
        self.initialLiveChatContents = liveChatContents.getLiveChatData()

    def generateInitialState(self):
        parser = livechatParser('html.parser')
        parser.buildParser(self.initialLiveChatContents)
        parser.findContent()
        self.playerState = PlayerState()
        self.playerState.continuation = parser.initialContinuation

    def parseSubsequentContents(self):
        subRequestor = SubsequentRequestor(self.videoId, self.playerState)
        subRequestor.buildFetcher()
        subRequestor.makeRequest()
        content = subRequestor.response["continuationContents"]["liveChatContinuation"]["actions"][1::]
        self.playerState.continuation = subRequestor.updateContinuation(subRequestor.response)
        for c in content:
            self.content += str(c["replayChatItemAction"])
            self.contentSet.append(c["replayChatItemAction"])
        self.playerState.playerOffsetMs = self.findOffsetTimeMsecFinal()

    def findOffsetTimeMsecFinal(self):
        finalContent = self.contentSet[-1]
        return finalContent["videoOffsetTimeMsec"]

    def outputContent(self):
        returnSet = []
        for c in self.contentSet:
            comment = ''
            timestamp = ''
            author = ''
            giftContent = False
            superChatContent = False
            if("addLiveChatTickerItemAction" in c["actions"][0] 
               or "addBannerToLiveChatCommand" in c["actions"][0] #pinned message
               or "liveChatMembershipItemRenderer" in c["actions"][0]["addChatItemAction"]["item"] #membership joined
               or "liveChatSponsorshipsGiftPurchaseAnnouncementRenderer" in c["actions"][0]["addChatItemAction"]["item"]  #gift membership purchased
               or "liveChatTickerSponsorItemRenderer" in c["actions"][0]["addChatItemAction"]["item"] #gift message
               ):
                giftContent = True
            elif("liveChatPaidMessageRenderer" in c["actions"][0]["addChatItemAction"]["item"]): #superchat
                superChatContent = True

            if not giftContent and not superChatContent:
                if("liveChatMembershipItemRenderer" in c["actions"][0]["addChatItemAction"]["item"]):
                    timestamp = c["actions"][0]["addChatItemAction"]["item"]["liveChatMembershipItemRenderer"]["timestampText"]["simpleText"] 
                    author = c["actions"][0]["addChatItemAction"]["item"]["liveChatMembershipItemRenderer"]["authorName"]["simpleText"]
                    comment = c["actions"][0]["addChatItemAction"]["item"]["liveChatMembershipItemRenderer"]["message"]["runs"][0]["text"]
                elif("emoji" in c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]):
                    timestamp = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]
                    author = c["actions"][0]["addChatItemAction"][ "item"]["liveChatTextMessageRenderer"]["authorName"]["simpleText"]
                    comment =  c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]["emoji"]["image"]["accessibility"]["accessibilityData"]["label"]
                else:
                    timestamp = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]
                    author = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["authorName"]["simpleText"]
                    comment = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]["text"]
                returnSet.append("({0}) {1}: {2} \n".format(timestamp, author, comment))
        return returnSet

    def outputMessages(self):
        messages = []
        for c in self.contentSet:
            payload = c["actions"][0]
            if(nc.tickerItemActionNode in payload):
                pass
            elif(nc.addBannerNode in payload):
                pinnedMessage = PinnedMessage(payload)
                pinnedMessage.buildMessage()
                messages.append(pinnedMessage.generateContent())
            elif(nc.liveChatPaidMessageNode in payload[nc.addChatItemActionNode][nc.itemNode]):
                superchat = superchatMessage(payload)
                superchat.buildMessage()
                messages.append(superchat.generateContent())
            elif(nc.liveChatMembershipNode in payload[nc.addChatItemActionNode][nc.itemNode]):
                membership = membershipChatMessage(payload)
                membership.buildMessage()
                messages.append(membership.generateContent())
            elif(nc.liveChatMembershipGiftPurchasedAnnouncementNode in payload[nc.addChatItemActionNode][nc.itemNode]):
                membershipGift = membershipGiftedMessage(payload)
                membershipGift.buildMessage()
                messages.append(membershipGift.generateContent())
            elif(nc.liveChatTextMessageRendererNode in payload[nc.addChatItemActionNode][nc.itemNode]):
                chat = chatMessage(payload)
                chat.buildMessage()
                messages.append(chat.generateContent())
        return messages

    def scrape(self):
        self.getContinuation()
        self.getInitialLiveChatContents()
        self.generateInitialState()
        self.endTime = int(self.getEndTime())
        self.parseSubsequentContents()
        while(int(self.playerState.playerOffsetMs) < self.endTime):
            try:
                self.parseSubsequentContents()
            except Exception as e:
                print("Exception encountered: {0}".format(str(e)))
                with open('output/output.txt', 'w+', encoding='utf-8') as writer:
                    writer.write(str(self.outputMessages))
        with open('output/output.txt', 'w', encoding='utf-8') as writer:
            returnSet = self.outputMessages()
            for r in returnSet:
                writer.write(r)

    def scrapeToFile(self):
        self.getContinuation()
        self.getInitialLiveChatContents()
        self.generateInitialState()
        self.endTime = int(self.getEndTime())
        self.parseSubsequentContents()
        while(int(self.playerState.playerOffsetMs) < self.endTime):
            try:
                self.parseSubsequentContents()
            except Exception as e:
                print("Exception encountered: {0}".format(str(e)))
                with open('output/output.txt', 'w+', encoding='utf-8') as writer:
                    writer.write(str(self.outputMessages))
        with open(f'output/scrape_{time.time()}.json', 'w', encoding='utf-8') as writer:
            writer.write(json.dumps(self.contentSet))

    def outputContentFromScrapedFile(self, filename):
        with open(f'output/{filename}', 'r', encoding='utf-8') as reader:
            self.contentSet = json.load(reader)
        
        self.outputMessages()
        
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
