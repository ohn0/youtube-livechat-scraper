from player_state import PlayerState

class ContinuationFetcher:
    params = {}
    playerState = None
    def __init__(self, videoId, pState = None):
        self.playerState = pState
        self.initializeParams(videoId)

    def initializeParams(self, videoId):
        self.params["context"] = self.initializeContext()

        if self.playerState != None:
            self.params["continuation"] = self.playerState.continuation
            self.params["currentPlayerState"] = {"playerOffsetMs" : str(self.playerState.playerOffsetMs)}
        else:
            self.params["videoId"] = videoId
            self.params["params"] = ""
            self.params["racyCheckOk"] = False
            self.params["contentCheckOk"] = False
            self.params["autonavState"] = "STATE_NONE"
            self.params["playbackContext"] = {}
            self.params["captionRequested"] = False

    def initializeContext(self):
        context = {}
        context["client"] = self.initializeClient()
        context["user"]= {"lockedSafetyMode" : False}
        context["request"] = {}
        context["clickTracking"] = {}
        context["adSignalsInfo"] = {}

        return context
    
    def initializeClient(self):
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
        client["mainAppWebInfo"] = {"graftUrl": "", "webDisplayMode" : "WEB_DISPLAY_MODE_BROWSER", "isWebNativeShareAvailable" : False}
        
        return client


        