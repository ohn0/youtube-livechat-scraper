""""LiveChatScraper class, used to scrape live chat data from a youtube stream."""
import time
from math import floor

import constants.nodeConstants as nc
import constants.scraperConstants as con
from builders.playerState import PlayerState
from generators.outputGenerator import outputGenerator
from messages.chatMessage import chatMessage
from messages.membershipGiftedMessage import membershipGiftedMessage
from messages.membershipmessage import membershipChatMessage
from messages.PinnedMessage import PinnedMessage
from messages.superchatMessage import superchatMessage
from requestors.subsequentRequestor import SubsequentRequestor
from scrapers.scraperInitializer import ScraperInitializer
from scrapers.video import Video

CONTINUATION_FETCH_BASE_URL = "https://www.youtube.com/youtubei/v1/next?"

class LiveChatScraper:
    """"entry point for live chat scraper, this is exposed object 
    that someone would use to scrape livechat contents"""
    video = None
    player_state = None
    contentSet = []
    content = ''
    currentOffsetTimeMsec = 0
    end_time = 0
    output_filename = 'outputContent.json'
    invalid_characters = ['<', '>', ':', '"', '/', '\\','|', '?', '*']
    is_debugging = False
    requestor = None
    sleepValue = 3
    initialization_successful = False

    def __init__(self, video_url, debug_mode = False):
        self.video = Video(None,video_url, None)
        self.is_debugging = debug_mode
        self.__extract_video_id()

    def __set_initial_parameters(self):
        try:
            self.player_state = PlayerState()
            self.player_state.continuation = ScraperInitializer()\
                .generateInitialState(self.video.video_id)
            initial_content = ScraperInitializer().generateInitialContent(self.video.video_url)
            self.video.video_title = self.__clean_filename(initial_content["videoDetails"]["title"])
            self.output_filename = f'{self.video.video_title}_{time.time()}'
            self.end_time = int(initial_content["streamingData"]["formats"][0]["approxDurationMs"])
            self.initialization_successful = True
        except Exception:
            print("error encountered attempting to set initial parameters.")

    def __extract_video_id(self):
        key_start = self.video.video_url.find('=')+1
        key_end = key_start + self.video.VIDEO_ID_LENGTH
        self.video.video_id = self.video.video_url[key_start:key_end]

    def __clean_filename(self, output_filename):
        for char in self.invalid_characters:
            output_filename = output_filename.replace(char, '')
        return output_filename

    def __parse_subsequent_contents(self):
        self.requestor.makeRequest()
        try:
            action_contents = self.requestor.response["continuationContents"]\
                ["liveChatContinuation"]["actions"][1::]
            for content in action_contents:
                self.contentSet.append(content["replayChatItemAction"])
            self.player_state.continuation = self.requestor.updateContinuation\
                (self.requestor.response)
            self.player_state.playerOffsetMs = self.__find_final_offset_time()
            self.requestor.update_fetcher\
                (self.player_state.continuation, self.player_state.playerOffsetMs)
        except KeyError:
            print(self.requestor.response)
            self.player_state.continuation = con.SCRAPE_FINISHED

    def __find_final_offset_time(self):
        final_content = self.contentSet[-1]
        return final_content["videoOffsetTimeMsec"]

    def scrape(self):
        """method to call scrape functionality and pull livechat data."""
        self.__set_initial_parameters()
        if not self.initialization_successful:
            print("Unable to initialize scraper successfully, quitting")
            return False
        self.requestor = SubsequentRequestor(self.video.video_id, self.player_state)
        self.requestor.build_fetcher()
        print('Beginning livechat scraping')
        self.__parse_subsequent_contents()
        has_slept = True
        current_interval = 0
        while(int(self.player_state.playerOffsetMs) < self.end_time and self.player_state.continuation != con.SCRAPE_FINISHED):
            try:
                progress = float(self.player_state.playerOffsetMs)/float(self.end_time)
                print(f'progress: {progress:.2%}', end="\r")
                floored_progress = floor(progress * 100)
                if current_interval != floored_progress:
                    has_slept = False
                if(floored_progress % 10 == 0 and not has_slept):
                    time.sleep(self.sleepValue)
                    current_interval = floored_progress
                    has_slept = True
                self.__parse_subsequent_contents()
            except Exception as ex:
                print("scraping failed")
                print(f"Exception encountered: {str(ex)}")
        print("scraping completed")
        return True

    def output_messages(self):
        """"build a messages list that contains all the chat messages"""
        messages = []
        for c in self.contentSet:
            payload = c[nc.actionsNode][0]
            if nc.tickerItemActionNode in payload:
                pass
            elif nc.addBannerNode in payload:
                pinned_message = PinnedMessage(payload)
                pinned_message.buildMessage()
                messages.append(pinned_message.generateContent())
            elif nc.liveChatPaidMessageNode in payload[nc.addChatItemActionNode][nc.itemNode]:
                superchat = superchatMessage(payload)
                superchat.buildMessage()
                messages.append(superchat.generateContent())
            elif nc.liveChatMembershipNode in payload[nc.addChatItemActionNode][nc.itemNode]:
                membership = membershipChatMessage(payload)
                membership.buildMessage()
                messages.append(membership.generateContent())
            elif nc.liveChatMembershipGiftPurchasedAnnouncementNode in payload[nc.addChatItemActionNode][nc.itemNode]:
                membership_gift = membershipGiftedMessage(payload)
                membership_gift.buildMessage()
                messages.append(membership_gift.generateContent())
            elif nc.liveChatTextMessageRendererNode in payload[nc.addChatItemActionNode][nc.itemNode]:
                chat = chatMessage(payload)
                chat.buildMessage()
                messages.append(chat.generateContent())
        return messages

    def write_to_file(self, write_type, output_filename = None):
        """"writes currently scraped content to a file output"""
        if output_filename is None:
            output_filename = f'{write_type}_{self.output_filename}'
        generator = outputGenerator(output_filename)
        if write_type != con.OUTPUT_RAW:
            generator.generate(self.output_messages(), write_type)
        else:
            generator.generate(self.contentSet, write_type)
