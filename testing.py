from inspect import cleandoc
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
scraper.scrapeToFile(cleanData=True)
#   output = scraper.outputContentFromScrapedFile('raw_output.json')

# with open('z', 'w', encoding='utf-8') as writer:
#     writer.write(json.dumps(output))

# output = scraper.outputContentFromScrapedFile("raw_output.json")
# scraper.writeContentToFile(json.dumps(output))
# scraper.generateCleanDataset(output)


endTime = time.time()
print(f'program runtime: {endTime - startTime}')

#output/cleaned_【COOKING SIMULATOR VR】 would you like dinner first? or maybe...♡ 【NIJISANJI EN | Elira Pendora】.txt
#title causing errors

# https://www.youtube.com/watch?v=FMV7p2j7pF4 【GOOSE GOOSE DUCK】 sussy honk I mean quack I mean 【NIJISANJI EN | Elira Pendora】