import asyncio
from typing import List
from entities.music import MusicEntity

from features.recommend_music.data import RecommendMusicRepository
from .base import BaseRecommendMusicUsecase

loop = asyncio.get_event_loop()

class UsecaseRecommendMusic(BaseRecommendMusicUsecase):
    def __init__(self):
        super().__init__()

    def execute(self, skip=0, limit=5) -> List[MusicEntity]:
        # Find top best musics
        # Sort creterias (from most important to less)
        # - shareCount
        # - commentCount
        # - diggCount
        # - playCount
        best_musics = loop.run_until_complete(self.repository.get_music(skip=skip, limit=limit))

        return best_musics