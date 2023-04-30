# youtube-livechat-scraper
A tool to scrape youtube livechat data I came up with while watching vtubers. It rips almost all data from a VOD's livechat including the following:
- Chat messages
- Superchats
- Memberships joined
- Memberships gifted and received

All of the data can be wrapped up in a large raw JSON object that also contains lots of metadata from the responses, like the author, the time the message got sent, etc.

## USAGE:

Requires the following python packages:
  
  - Python3
  - BeautifulSoup
  - Requests
  
- Import the LiveChatScraper from scrapers.liveChatScraper to wherever you want to make the scraping call.
- Find a VOD URL and copy it
- Create a LiveChatScraper object and pass in the VOD's URL.
- Call the scrape() method on the created scraper object and the scrape will run.
- Once the scrape is completed, you can call ouputMessages() to get a dictionary with all the scraped data.
- You can all save the scraped data as a JSON to a fill by calling the writeToFile method passing the OUTPUT_JSON constant

* example.py has a working example which saves the data to different formats


  
  
  
