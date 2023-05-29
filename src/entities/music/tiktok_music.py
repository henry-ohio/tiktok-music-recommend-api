from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class TiktokMusicEntity:
    id: Optional[str] = None
    music_id: Optional[str] = None # FK to Music Entity
    tiktok_id: str
    is_original: bool
    album: str
    play_url: str
    cover_medium_url: str