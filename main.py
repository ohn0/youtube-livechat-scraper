from scrapers.liveChatScraper import LiveChatScraper
import constants.scraperConstants as sCons
import sys
import time

if(len(sys.argv) == 1):
    print("Insufficient number of arguments entered.")
    sys.exit()


def testScraperOutputToJson():
    startTime = time.time()
    videoUrl = sys.argv[1]
    scraper = LiveChatScraper(videoUrl)
    scraper.scrape()
    scrapedContent = scraper.outputMessages()
    scraper.writeToFile(sCons.OUTPUT_JSON)
    endTime = time.time()
    print(f'program runtime: {endTime - startTime}')

testScraperOutputToJson()
