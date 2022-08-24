# YT-livechat-scraper
A dumb tool I made while watching vtubers, scrapes all livechat data from an existing VOD.

grab youtube chat data

USAGE:
  This tool works in python3, download the project and open a terminal in the root directory.
  
  Run the main.py script and add the Youtube video URL of the VOD whose livechat you want to scrape.
  
  ex: python main.py https://www.youtube.com/watch?v=sAaudXJ5IjU
  
  Let the program run, once it finishes, a text file will be generated in the output folder containing the scraped contents in one file.

This is a python tool for scraping Youtube Livechat data from VOD streams. 
Currently it works on completed streams, scraping livestream live chat is planned.
The tool scrapes an existing VOD's livechat and outputs all the messages, superchat message and price, memberships joined, membership gifts, and membership messages 
generated during the livestream.
Currently the tool outputs all the data into a textfile with each line containing a message, the length of time since the stream began, and the author of the message.



I plan on adding separated contents and JSON output for the scraped set.

Requires the following python packages:
  BeautifulSoup
  Requests
  
  
  
