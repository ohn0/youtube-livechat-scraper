from liveChatScraper import LiveChatScraper
import scraperConstants as sCons
import sys
import time

startTime = time.time()
if(len(sys.argv) == 1):
    print("Insufficient number of arguments entered.")
    sys.exit()
videoUrl = sys.argv[1]
scraper = LiveChatScraper(videoUrl)
scraper.scrape()
scrapedContent = scraper.outputMessages()
scraper.writeToFile(sCons.OUTPUT_JSON)
endTime = time.time()
print(f'program runtime: {endTime - startTime}')