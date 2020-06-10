class BeatMap:
    def __init__(self, key, difficulty, up_votes, down_votes, downloads, heat, map_rating, bpm, map_file=None, audio_file=None):
        self.key = key
        self.difficulty = difficulty
        self.up_votes = up_votes
        self.down_votes = down_votes
        self.downloads = downloads
        self.heat = heat
        self.map_rating = map_rating
        self.bpm = bpm
        self.map_file = map_file
        self.audio_file = audio_file
