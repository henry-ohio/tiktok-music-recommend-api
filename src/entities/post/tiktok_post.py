from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass(kw_only=True)
class TikTokPostEntity:
    id: Optional[str] = None
    tiktok_id: str
    web_video_url: str
    digg_count: int
    share_count: int
    play_count: int
    comment_count: int
    tiktok_location: str
    author_id: str # PK to author
    video_id: str # PK to video
    music_id: str # PK to music