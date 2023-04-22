from scrapers.liveChatScraper import LiveChatScraper
import constants.scraperConstants as sCons
import sys
import time

def testScraperOutput(videoUrl):
    startTime = time.time()
    scraper = LiveChatScraper(videoUrl)
    scraper.scrape()
    scrapedContent = scraper.outputMessages()
    # saves all messages in a file as a json object
    scraper.writeToFile(sCons.OUTPUT_JSON, "testJson_"+scraper.outputFileName)
    # saves all messages in a txt file, each line is a message entry
    scraper.writeToFile(sCons.OUTPUT_TEXT, "testText_"+scraper.outputFileName)
    # saves all messages in a json file preserving the raw json that comes over when making the request call to youtube
    scraper.writeToFile(sCons.OUTPUT_RAW, "testRaw_"+scraper.outputFileName)
    endTime = time.time()
    print(f'program runtime: {endTime - startTime}')

if(len(sys.argv) == 1):
    sampleVideoUrl = "https://www.youtube.com/watch?v=MNraBP_LoNM"
    testScraperOutput(sampleVideoUrl)
else:
    testScraperOutput(sys.argv[1])

