from dataclasses import dataclass
from typing import List

@dataclass
class TikTokPostEntity:
    id: str
    web_video_url: str
    media_urls: List[str]
    digg_count: int
    share_count: int
    play_count: int
    comment_count: int
    mentions: List
    hashtag: List
    author_id: str # PK to author
    video_id: str # PK to video
    music_id: str # PK to music