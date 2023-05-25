from dataclasses import dataclass

@dataclass
class VideoEntity:
    id: str
    original_download_address: str
    download_address: str
    format: str
    definition: str
    tiktok_cover: str
    tiktok_original_cover: str
    width: int
    height: int
    duration: float
