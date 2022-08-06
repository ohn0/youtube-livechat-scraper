class PlayerState:
    playerOffsetMs = 0
    delta = 30000
    continuation = ''

    def updateDelta(self, newDelta, continuation):
        self.delta = newDelta
        self.continuation = continuation

    def getNextOffset(self):
        self.playerOffsetMs += self.delta

    