"""contains state of player tracking the scrape"""
class PlayerState:
    """PlayerState holds the current state of the scrape, where\
 it's location is in the stream."""
    player_offset_ms = 0
    delta = 30000
    continuation = ''

    def update_delta(self, new_delta, continuation):
        """updates the delta value and continuation values"""
        self.delta = new_delta
        self.continuation = continuation

    def get_next_offset(self):
        """returns the next offset to be used in the scrape"""
        self.player_offset_ms += self.delta
