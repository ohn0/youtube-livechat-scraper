class Video:
    """"Video object container"""
    video_id = None
    video_url = ''
    video_title = ''
    VIDEO_ID_LENGTH = 11

    def __init__(self, video_id, url, title):
        self.video_id = video_id
        self.video_url = url
        self.video_title = title
