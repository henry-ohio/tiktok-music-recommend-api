
from .dao.music_dao import MusicDAO, TikTokMusicDAO
from .dao.author_dao import AuthorDAO
from .dao.video_dao import VideoDAO

class RecommendMusicRepository:
    def __init__(self) -> None:
        self.author_dao = AuthorDAO()
        self.music_dao = MusicDAO()
        self.tiktok_music_dao = TikTokMusicDAO()
        self.video_dao = VideoDAO()

    def crawl_tiktok_data(self):
        """
        Crawl data from Tiktok API, save to database

        TODO: for now, use mock json data
        """

    
    def get_music(self, sort_by=None, skip=0, limit=1):
        """
        Get music recommendation
        TODO: For now, just do simple ranking by scoring.
        """
