from features.recommend_music.data import RecommendMusicRepository
from .base import BaseRecommendMusicUsecase

class UsecaseRecommendMusic(BaseRecommendMusicUsecase):
    def __init__(self):
        super().__init__()

    def execute(self):
        best_musics = self.repository.get_music(sorted_by='score') 

        return best_musics