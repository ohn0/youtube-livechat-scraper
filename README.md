# youtube-livechat-scraper
A dumb tool I made while watching vtubers, scrapes all livechat data from an existing VOD for anyone who wants to look.
  
  The tool scrapes an existing VOD's livechat and outputs all the messages, superchat message and price, memberships joined, membership gifts, and membership messages.
  

USAGE:

Requires the following python packages:
  
  BeautifulSoup
  
  Requests
  
  This tool works in python3, download the project and open a terminal in the root directory.
  
  Run the main.py script and add the Youtube video URL of the VOD whose livechat you want to scrape.
  
  ex: python main.py https://www.youtube.com/watch?v=sAaudXJ5IjU
  
  the default version will output the contents into a JSON array, with object being a chat element(message, superchat, etc.)

  Currently it works on completed streams, scraping livestream live chat is planned.


  
  
  
