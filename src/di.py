from kink import di
from config import SQLSettings

from .features.recommend_music import init_di as recommend_music_init_di

def init_di():
    di[SQLSettings] = SQLSettings()
    
    recommend_music_init_di()