from .base import BaseRecommendMusicUsecase

class UsecaseRecommendMusic(BaseRecommendMusicUsecase):
    def __init__(self) -> None:
        pass

    def execute(self):
        best_musics = self.repository.get_music(sorted_by='score') 

        return best_musics