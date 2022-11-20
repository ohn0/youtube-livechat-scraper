from fileinput import filename
import nodeConstants as nc
import scraperConstants as con
from playerState import PlayerState
from subsequentRequestor import SubsequentRequestor
from messages.PinnedMessage import PinnedMessage
from messages.superchatMessage import superchatMessage
from messages.membershipmessage import membershipChatMessage
from messages.membershipGiftedMessage import membershipGiftedMessage
from messages.chatMessage import chatMessage
from outputGenerator import outputGenerator
from scraperInitializer import ScraperInitializer
import json
import time
from math import floor

CONTINUATION_FETCH_BASE_URL = "https://www.youtube.com/youtubei/v1/next?"

class LiveChatScraper:
    videoId = None
    videoUrl = None
    playerState = None
    contentSet = []
    content = ''
    currentOffsetTimeMsec = 0
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
        self.playerState = PlayerState()
        self.playerState.continuation = ScraperInitializer().generateInitialState(self.videoId)
        initialContent = ScraperInitializer().generateInitialContent(self.videoUrl)
        self.videoTitle = self.cleanFilename(initialContent["videoDetails"]["title"])
        self.outputFileName = f'{self.videoTitle}_{time.time()}'
        self.generator.outputName = self.videoTitle;
        self.endTime = int(initialContent["streamingData"]["formats"][0]["approxDurationMs"])

    def extractVideoID(self, videoUrl):
        keyStart = videoUrl.find('=')+1
        keyEnd = keyStart + self.VIDEO_ID_LENGTH
        self.videoId = videoUrl[keyStart:keyEnd]

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

    def scrape(self):
        self.setInitialParameters()
        self.requestor = SubsequentRequestor(self.videoId, self.playerState)
        self.requestor.buildFetcher()
        print('Beginning livechat scraping')
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
                print("scraping failed")
                print("Exception encountered: {0}".format(str(e)))
        print("scraping completed")

    def outputMessages(self):
        messages = []
        for c in self.contentSet:
            payload = c[nc.actionsNode][0]
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

    def writeToFile(self, writeType, fileName = None):
        if(fileName == None):
            fileName = f'{writeType}_{self.outputFileName}'
        generator = outputGenerator(fileName)
        if(writeType != con.OUTPUT_RAW):
            generator.generate(self.outputMessages(), writeType)
        else:
            generator.generate(self.contentSet, writeType)
