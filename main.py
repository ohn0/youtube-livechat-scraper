from inspect import cleandoc
from liveChatScraper import LiveChatScraper
import sys
import time
startTime = time.time()
if(len(sys.argv) == 1):
    print("Insufficient number of arguments entered.")
    sys.exit()
videoUrl = sys.argv[1]
scraper = LiveChatScraper(videoUrl)
scraper.scrapeToFile()

endTime = time.time()
print(f'program runtime: {endTime - startTime}')