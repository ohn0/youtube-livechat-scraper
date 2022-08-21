class Extractor:
    liveChatTickerAction =          "addLiveChatTickerItemAction"
    pinnedLiveChatAction =          "addBannerToLiveChatCommand"
    membershipJoinedAction =        "liveChatMembershipItemRenderer"
    membershipGiftPurchasedAction = "liveChatSponsorshipsGiftPurchaseAnnouncementRenderer"
    membershipGiftRedeemed =        "liveChatTickerSponsorItemRenderer"
    superChatAction =               "liveChatPaidMessageRenderer"
    memberShipMessageAction =       "liveChatMembershipItemRenderer"
    emojiAction =                   "emoji"
    liveChatAction =                ""

    
    def __init__(self):
        pass

    def extractContent(self, contents):
        messages = []

        for content in contents:
            pass
