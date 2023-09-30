from livechat_scraper.constants import node_constants as nc
from livechat_scraper.messages.chat_message import ChatMessage
from livechat_scraper.messages.membership_gifted_message import MembershipGiftedMessage
from livechat_scraper.messages.membership_message import MembershipChatMessage
from livechat_scraper.messages.pinned_message import PinnedMessage
from livechat_scraper.messages.superchat_message import SuperChatMessage
from livechat_scraper.messages.message import Message
from livechat_scraper.messages.membership_redeemed_message import MembershipRedeemedMessage
from livechat_scraper.messages.purchased_sticker_message import PurchasedSticker
class messageFactory():
    """
    Factory class to build Messages, pass in a payload that contains liveChatPaidMessageRenderer,
    addBannerToLiveChatCommand, liveChatMembershipItemRenderer, 
    liveChatSponsorshipsGiftPurchaseAnnouncementRenderer, liveChatTextMessageRenderer JSON objects
    and the factory will return a Message object of the correct type
    """
    def __init__(self):
        self.build_from_items = {
            nc.LIVECHAT_PAID_MESSAGE_NODE: lambda pl: SuperChatMessage(pl),
            nc.LIVECHAT_MEMBERSHIP_NODE: lambda pl: MembershipChatMessage(pl),
            nc.LIVECHAT_MEMBERSHIP_GIFT_PURCHASED_ANNOUNCEMENT_NODE: lambda pl: MembershipGiftedMessage(pl),
            nc.LIVECHAT_TEXT_MESSAGE_RENDERER_NODE: lambda pl: ChatMessage(pl),
            nc.LIVECHAT_MEMBERSHIP_GIFT_RECEIVED_ANNOUNCEMENT_NODE: lambda pl: MembershipRedeemedMessage(pl),
            nc.LIVECHAT_PAID_STICKER_RENDERER : lambda pl: PurchasedSticker(pl)
        }

        self.build_from_root = {
            nc.ADD_BANNER_NODE: lambda pl: PinnedMessage(pl)
        }


    def build(self, payload) -> Message:
        """factory to build a Message given a payload fragment"""
        for m_type, builder in self.build_from_root.items():
            if m_type in payload:
                return builder(payload)

        for m_type, builder in self.build_from_items.items():
            if m_type in payload[nc.ADD_CHAT_ITEM_ACTION_NODE][nc.ITEM_NODE]:
                return builder(payload)

        print(payload)