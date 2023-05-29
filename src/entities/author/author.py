from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class AuthorEntity:
    id: Optional[str] = None
    name: str
    tiktok_id: str
    tiktok_nickname: str
    tiktok_display_name: str
    tiktok_signnature: str
    tiktok_avatar: str
    tiktok_is_private_account: bool
    tiktok_is_verified: bool