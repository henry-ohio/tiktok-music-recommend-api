from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class MusicEntity:
    id: Optional[str] = None
    name: str
    author_name: str
    total_digg_count: int 
    total_share_count: int
    total_play_count: int
    total_comment_count: int