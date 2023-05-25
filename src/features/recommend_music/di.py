from kink import di
from .data import RecommendMusicRepository

def init_di():
    di[RecommendMusicRepository] = RecommendMusicRepository()