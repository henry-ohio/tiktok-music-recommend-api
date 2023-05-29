from features.recommend_music.data import RecommendMusicRepository
from .base import BaseRecommendMusicUsecase

class UsecaseRecommendMusic(BaseRecommendMusicUsecase):
    def __init__(self):
        super().__init__()

    def execute(self):
        # Find top best musics
        # Sort creterias (from most important to less)
        # - shareCount
        # - commentCount
        # - diggCount
        # - playCount
        best_musics = self.repository.get_music()

        return best_musics