"""module for a livechat parser that takes a raw response json from youtube and will
parse out the relevant chat data that is needed for the output."""
import json

from bs4 import BeautifulSoup


class LivechatParser:
    """LivechatParser class takes a raw response from youtube and pulls out relevant content 
    for data we are looking for(livechat info, superchats, memberships)"""
    parse_type = ""
    soup_parser = None
    livechat_contents = None
    initial_continuation = None

    def __init__(self, parse_type):
        self.parse_type = parse_type

    def build_parser(self, livechat_data):
        """returns a BeautifulSoup parser for content extraction."""
        self.soup_parser = BeautifulSoup(livechat_data.text, self.parse_type)

    def find_content(self):
        """parser seeks out the content where the livechat data for output resides 
        in the raw response"""
        scripts = self.soup_parser.find_all('script')
        content = str([x for x in scripts if "authorName" in x.text][0])
        start_index = content.find('{')
        end_index = len(content) - content[::-1].find('}')
        self.livechat_contents = json.loads(content[start_index:end_index])
        self.initial_continuation = self.livechat_contents["continuationContents"]\
            ["liveChatContinuation"]["header"]["liveChatHeaderRenderer"]["viewSelector"]\
                ["sortFilterSubMenuRenderer"]["subMenuItems"][1]["continuation"]\
                    ["reloadContinuationData"]["continuation"]
        return self.livechat_contents["continuationContents"]["liveChatContinuation"]["actions"]
