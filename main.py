from liveChatScraper import LiveChatScraper
import sys
import time
import json

startTime = time.time()
if(len(sys.argv) == 1):
    print("Insufficient number of arguments entered.")
    sys.exit()
videoUrl = sys.argv[1]
scraper = LiveChatScraper(videoUrl)
# scraper.scrapeToFile()
scrapedContent = scraper.outputContentFromScrapedFile('scrape_1661086761.3118222.json')
scraper.writeContentToFile(json.dumps(scrapedContent))
endTime = time.time()
print(f'program runtime: {endTime - startTime}')