"""holds fetcher object used to store params for POST calls"""
class ContinuationFetcher:
    """class used to build an object that holds all\
 the parameters to pass for fetching livechat data"""
    params = {}
    player_state = None
    def __init__(self, video_id, player_state = None):
        self.player_state = player_state
        self.intialize_params(video_id)

    def intialize_params(self, video_id):
        """configure params for POST call to initial values."""
        self.params["context"] = self.__initialize_context()

        if self.player_state is not None:
            self.params["continuation"] = self.player_state.continuation
            self.params["currentPlayerState"] = \
                {"playerOffsetMs" : str(self.player_state.playerOffsetMs)}
        else:
            self.params["videoId"] = video_id
            self.params["params"] = ""
            self.params["racyCheckOk"] = False
            self.params["contentCheckOk"] = False
            self.params["autonavState"] = "STATE_NONE"
            self.params["playbackContext"] = {}
            self.params["captionRequested"] = False

    def __initialize_context(self):
        context = {}
        context["client"] = self.__initialize_client()
        context["user"]= {"lockedSafetyMode" : False}
        context["request"] = {}
        context["clickTracking"] = {}
        context["adSignalsInfo"] = {}

        return context

    def __initialize_client(self):
        client = {}
        client["hl"] = "en"
        client["gl"] = "US"
        client["visitorData"] = ""
        client["remoteHost"] = ""
        client["deviceMake"] = ""
        client["deviceModel"] = ""
        client["userAgent"] = ""
        client["clientName"] = "WEB"
        client["clientVersion"] = "2.20220801.00.00"
        client["osName"] = ""
        client["osVersion"] = ""
        client["originalUrl"] = ""
        client["platform"] = "DESKTOP"
        client["clientFormFactor"] = "UNKNOWN_FORM_FACTOR"
        client["configInfo"] = {"appInstallData" : ""}
        client["userInterfaceTheme"] = "USER_INTERFACE_THEME_DARK"
        client["timezone"] = ""
        client["browserName"] = ""
        client["browserVersion"] = ""
        client["screenWidthPoints"] = "1920"
        client["screenHeightPoints"] = "955"
        client["screenPixelDensity"] = 1
        client["screenDensityFloat"] = 1
        client["utcOffsetMinutes"] = -240
        client["clientScreen"] = "WATCH"
        client["mainAppWebInfo"] = {"graftUrl": "", "webDisplayMode" : "WEB_DISPLAY_MODE_BROWSER"\
            , "isWebNativeShareAvailable" : False}

        return client
