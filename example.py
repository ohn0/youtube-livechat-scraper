from scrapers.liveChatScraper import LiveChatScraper
import constants.scraperConstants as sCons
import sys
import time

def testScraperOutputToJson(videoUrl):
    startTime = time.time()
    scraper = LiveChatScraper(videoUrl)
    scraper.scrape()
    scrapedContent = scraper.outputMessages()
    scraper.writeToFile(sCons.OUTPUT_JSON)
    endTime = time.time()
    print(f'program runtime: {endTime - startTime}')

if(len(sys.argv) == 1):
    sampleVideoUrl = "https://www.youtube.com/watch?v=MNraBP_LoNM"
    testScraperOutputToJson(sampleVideoUrl)
else:
    testScraperOutputToJson(sys.argv[1])

