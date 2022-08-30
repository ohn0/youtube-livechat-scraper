from fileinput import filename
import nodeConstants as nc
import constants as con
from continuationRequestor import ContinuationRequestor
from livechatRequestor import livechatRequestor
from livechatParser import livechatParser
from playerState import PlayerState
from subsequentRequestor import SubsequentRequestor
from initialDocumentExtractor import initialExtractor
from initialDocumentRequestor import initialDocumentRequestor
from PinnedMessage import PinnedMessage
from superchatMessage import superchatMessage
from membershipmessage import membershipChatMessage
from membershipGiftedMessage import membershipGiftedMessage
from chatMessage import chatMessage
from outputGenerator import outputGenerator
import json
import time
from math import floor

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
    videoTitle = ''
    outputFileName = 'outputContent.json'
    VIDEO_ID_LENGTH = 11
    invalid_characters = ['<', '>', ':', '"', '/', '\\','|', '?', '*']
    isDebugging = False
    generator = None
    requestor = None
    sleepValue = 3

    def __init__(self, videoUrl, debugMode = False):
        self.videoUrl= videoUrl
        self.isDebugging = debugMode
        self.extractVideoID(videoUrl)
        self.generator = outputGenerator()

    def setInitialParameters(self):
        documentRequestor = initialDocumentRequestor()
        initialDocument = documentRequestor.getContent(self.videoUrl)
        endTimeSeeker = initialExtractor()
        initialContent = endTimeSeeker.buildAndGetScript(initialDocument.text)
        self.videoTitle = self.cleanFilename(initialContent["videoDetails"]["title"])
        self.outputFileName = f'{self.videoTitle}_{time.time()}.json'
        self.generator.outputName = self.videoTitle;
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

    def cleanFilename(self, filename):
        for c in self.invalid_characters:
            filename = filename.replace(c, '')
        return filename

    def parseSubsequentContents(self):
        self.requestor.makeRequest()
        try:
            content = self.requestor.response["continuationContents"]["liveChatContinuation"]["actions"][1::]
            for c in content:
                self.contentSet.append(c["replayChatItemAction"])
            
            self.playerState.continuation = self.requestor.updateContinuation(self.requestor.response)
            self.playerState.playerOffsetMs = self.findOffsetTimeMsecFinal()
            self.requestor.updateFetcher(self.playerState.continuation, self.playerState.playerOffsetMs)
        except KeyError:
            print(self.requestor.response)
            self.playerState.continuation = con.SCRAPE_FINISHED


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
        self.endTime = int(self.setInitialParameters())
        self.requestor = SubsequentRequestor(self.videoId, self.playerState)
        self.requestor.buildFetcher()
        print('Beginning to make web calls to get livechat data')
        self.parseSubsequentContents()
        hasSlept = True
        currentInterval = 0
        while(int(self.playerState.playerOffsetMs) < self.endTime and self.playerState.continuation != con.SCRAPE_FINISHED):
            try:
                progress = float(self.playerState.playerOffsetMs)/float(self.endTime)
                print(f'progress: {progress:.2%}', end="\r")
                flooredProgress = floor(progress * 100)
                if(currentInterval != flooredProgress):
                    hasSlept = False
                if(flooredProgress % 10 == 0 and not hasSlept):
                    time.sleep(self.sleepValue)
                    currentInterval = flooredProgress
                    hasSlept = True
                self.parseSubsequentContents()
            except Exception as e:
                print("Exception encountered: {0}".format(str(e)))
                self.writeContentToFile(str(self.outputMessages))

    def scrapeToFile(self, cleanData = False):
        self.scrape()
        if(self.isDebugging):
            self.writeContentToFile(json.dumps(self.contentSet), 'raw_output.json')
        output = self.outputMessages()
        if(cleanData):
            self.generator.generate(output, con.OUTPUT_TEXT)
        else:
            self.generator.generate(output, con.OUTPUT_JSON)

    def outputContentFromScrapedFile(self, filename):
        with open(filename, 'r+', encoding='utf-8') as reader:
            self.contentSet = json.load(reader)
        return self.outputMessages()

    def writeContentToFile(self, scrapedContent, fileName = None):
        if(fileName == None):
            fileName = self.outputFileName
        with open(fileName, 'w+', encoding='utf-8') as writer:
            writer.write(scrapedContent)

    def generateCleanDataset(self, dataset):
        resultSet = []
        outputLocation = "scraped_"+self.outputFileName+".txt" 
        with open(outputLocation, 'w', encoding='utf-8') as writer:
            for content in dataset:
                if("purchaseAmount" in content["content"]):
                    resultSet.append(f'({content["occurrenceTimestamp"]} {content["author"]} purchased superchat({content["content"]["purchaseAmount"]["simpleText"]}) with message:\n\t{content["content"]["message"]}\n')
                elif("membershipChat" in content["content"]):
                    resultSet.append(f'({content["occurrenceTimestamp"]}) {content["author"]} : {content["content"]["membershipChat"]}\n')
                elif("membershipJoin" in content["content"]):
                    resultSet.append(f'({content["occurrenceTimestamp"]}) ({content["author"]}) joined membership!\n')
                elif("message" in content["content"]):
                    resultSet.append(f'({content["occurrenceTimestamp"]}) {content["author"]} : {content["content"]["message"]}\n')
            writer.writelines(resultSet)    


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

    step 4:
        Once all livechat blocks are obtained, we can write them out to a file.
'''
