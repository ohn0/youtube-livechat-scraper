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
output = scraper.outputContentFromScrapedFile('scrape_1661086761.3118222.json')
with open('output/chat_output.json', 'w', encoding='utf-8') as writer:
    writer.write(json.dumps(output))
endTime = time.time()
print(f'program runtime: {endTime - startTime}')