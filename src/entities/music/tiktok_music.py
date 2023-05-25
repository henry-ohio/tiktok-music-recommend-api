from dataclasses import dataclass

@dataclass
class TiktokMusicEntity:
    id: str
    music_id: str # FK to Music Entity
    tiktok_music_id: str
    tiktok_name: str
    author_name: str
    is_original: bool
    album: str
    play_url: str
    cover_medium_url: str