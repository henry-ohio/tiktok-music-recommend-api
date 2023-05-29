from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class VideoEntity:
    id: Optional[str] = None
    original_download_address: str
    download_address: str
    format: str
    definition: str
    tiktok_cover: str
    tiktok_original_cover: str
    width: int
    height: int
    duration: float
