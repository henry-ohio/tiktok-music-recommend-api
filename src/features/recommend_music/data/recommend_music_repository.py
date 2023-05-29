import os, json
from typing import Tuple

from loguru import logger
from dataclasses import asdict
from .dao.music_dao import MusicDAO, TikTokMusicDAO
from .dao.author_dao import AuthorDAO
from .dao.video_dao import VideoDAO
from .dao.tiktok_post_dao import TikTokPostDAO

from entities.post import TikTokPostEntity
from entities.author import AuthorEntity
from entities.music import MusicEntity, TiktokMusicEntity
from entities.video import VideoEntity

MOCK_DATA_DIR = "scripts/mock"

class RecommendMusicRepository:
    def __init__(self) -> None:
        self.author_dao = AuthorDAO()
        self.music_dao = MusicDAO()
        self.tiktok_music_dao = TikTokMusicDAO()
        self.video_dao = VideoDAO()
        self.tiktok_post_dao = TikTokPostDAO()

    async def crawl_tiktok_data(self):
        """
        Crawl data from Tiktok API, save to database

        TODO: for now, use mock json data
        """
        mock_data = []
        for mock_file in os.listdir(MOCK_DATA_DIR):
            if (mock_file.endswith('.json')):
                with open(os.path.join(MOCK_DATA_DIR, mock_file), 'r', encoding='utf8') as f:
                    data = json.load(f)
                    mock_data.extend(data)
        
        return mock_data
        
    async def save_tiktok_post(self, tiktok_post: TikTokPostEntity) -> TikTokPostEntity:
        """
        Write tiktok post to db
        """
        instance = await self.tiktok_post_dao.save(self.tiktok_post_dao.create(**asdict(tiktok_post)))
        return instance
    
    async def update_tiktok_post(self, tiktok_post: TikTokPostEntity) -> TikTokPostEntity:
        """
        Write tiktok post to db
        """
        instance = await self.tiktok_post_dao.save(tiktok_post)
        return instance


    async def save_music(self, music: MusicEntity, tiktok_music: TiktokMusicEntity) -> Tuple[MusicEntity, TiktokMusicEntity]:
        """
        Write music to db
        """
        music_instance = await self.music_dao.save(self.music_dao.create(**asdict(music)))
        tiktok_music.music_id = music_instance.id
        tiktok_music_instance = await self.tiktok_music_dao.save(self.tiktok_music_dao.create(**asdict(tiktok_music)))
        return music_instance, tiktok_music_instance
    
    async def update_music(self, music: MusicEntity) -> MusicEntity:
        """
        Update music to db
        """
        music_instance = await self.music_dao.save(music)
        return music_instance

    async def save_author(self, author: AuthorEntity) -> AuthorEntity:
        """
        Write author to db
        """
        instance = await self.author_dao.save(self.author_dao.create(**asdict(author)))
        return instance
    
    async def update_author(self, author: AuthorEntity, **kwargs) -> AuthorEntity:
        """
        Write author to db
        """
        instance = await self.author_dao.save(self.author_dao.merge(author, **kwargs))
        return instance
    
    async def get_author_by_tiktok_id(self, tiktok_id: str) -> AuthorEntity:
        """
        Get author
        """
        instance = await self.author_dao.find_one_or_none(tiktok_id=tiktok_id)
        return instance

    async def save_video(self, video: VideoEntity) -> MusicEntity:
        """
        Write video to db
        """
        instance = await self.video_dao.save(self.video_dao.create(**asdict(video)))
        return instance

    
    async def get_music(self, sort_by=None, skip=0, limit=1):
        """
        Get music recommendation
        TODO: For now, just do simple ranking by scoring.
        """

    async def get_post_by_tiktok_id(self, tiktok_id):
        tiktok_post = await self.tiktok_post_dao.find_one_or_none(tiktok_id=tiktok_id)
        return tiktok_post

    async def get_music_by_tiktok_id(self, tiktok_id):
        tiktok_music = await self.tiktok_music_dao.find_one_or_none(tiktok_id=tiktok_id)
        if tiktok_music is None:
            return None, None
        music = await self.music_dao.find_one_or_none(id=tiktok_music.music_id)
        return music, tiktok_music