from features.recommend_music.data import RecommendMusicRepository
from .base import BaseRecommendMusicUsecase

class UsecaseCrawlAndAnalyzeTikTokData(BaseRecommendMusicUsecase):
    def __init__(self):
        super().__init__()

    def execute(self):
        """
        Crawl tiktok data, then analyze and add some score for ranking
        """
        tiktok_posts = self.repository.crawl_tiktok_data()
        # TODO analyze and scoring
        