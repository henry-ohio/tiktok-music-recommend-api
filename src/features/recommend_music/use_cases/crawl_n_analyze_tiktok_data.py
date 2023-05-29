import asyncio

from features.recommend_music.data import RecommendMusicRepository

from entities.music import MusicEntity, TiktokMusicEntity
from entities.video import VideoEntity
from entities.author import AuthorEntity
from entities.post import TikTokPostEntity

from .base import BaseRecommendMusicUsecase

loop = asyncio.get_event_loop()

class UsecaseCrawlAndAnalyzeTikTokData(BaseRecommendMusicUsecase):
    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs):
        return loop.run_until_complete(self.__execute(*args, **kwargs))

    async def __execute(self, *args, **kwargs):
        """
        Crawl tiktok data, then analyze and add some score for ranking
        Return len of posts crawled
        """
        tiktok_posts = await self.repository.crawl_tiktok_data()

        # Write to database
        # TODO run in parralel. Right now, run in sequence to prevent racing condition.
        for post_data in tiktok_posts:
            await self.__save_one_post(post_data)

        return len(tiktok_posts)
        

    async def __save_one_post(self, post_data):
        """
        Check if the post exist in our database:
        - If existed, update, and update the music metadata
        - If no, insert
        Check if music existed in our database
        - If no, insert
        - If yes, update the counts
        """
        post = await self.repository.get_post_by_tiktok_id(post_data['id'])
        music_meta = post_data['musicMeta']
        music, tiktok_music = await self.repository.get_music_by_tiktok_id(music_meta['musicId'])

        digg_count = post_data["diggCount"] 
        share_count = post_data["shareCount"]
        play_count = post_data["playCount"]
        comment_count = post_data["commentCount"]

        if music is not None:
            # Update only
            # If new post, then add the count
            # If existing post, subtract the counts first, then add (to update latest count only)

            # TODO prevent racing condition here
            if post is None:
                # New post use this music
                music.total_digg_count = music.total_digg_count + digg_count
                music.total_share_count = music.total_share_count + share_count
                music.total_play_count = music.total_play_count + play_count
                music.total_comment_count = music.total_comment_count + comment_count
            else:
                music.total_digg_count = music.total_digg_count - post.digg_count + digg_count
                music.total_share_count = music.total_share_count - post.share_count + share_count
                music.total_play_count = music.total_play_count - post.play_count + play_count
                music.total_comment_count = music.total_comment_count - post.comment_count + comment_count

                self.repository.update_music(music)
        else:
            # Insert new music
            music = MusicEntity(
                name=music_meta['musicName'],
                author_name=music_meta['musicAuthor'],
                total_digg_count=digg_count, 
                total_share_count=share_count,
                total_play_count=play_count,
                total_comment_count=comment_count
            )

            tiktok_music = TiktokMusicEntity(
                tiktok_id=music_meta['musicId'],
                is_original=music_meta['musicOriginal'],
                album=music_meta['musicAlbum'],
                play_url=music_meta['playUrl'],
                cover_medium_url=music_meta['coverMediumUrl']
            )
        
            music, tiktok_music = await self.repository.save_music(music, tiktok_music)
        
        video_meta = post_data['videoMeta']
        video = VideoEntity(
            height=video_meta["height"],
            width=video_meta["width"],
            duration=video_meta["duration"],
            tiktok_cover=video_meta["coverUrl"],
            tiktok_original_cover=video_meta["originalCoverUrl"],
            definition=video_meta["definition"],
            format=video_meta["format"],
            original_download_address=video_meta["originalDownloadAddr"],
            download_address=video_meta["downloadAddr"]
        )
        video = await self.repository.save_video(video)

        author_meta = post_data['authorMeta']
        author = await self.repository.get_author_by_tiktok_id(author_meta['id'])
        if author is None:
            author = AuthorEntity(
                tiktok_id=author_meta['id'],
                name=author_meta['name'],
                tiktok_display_name=author_meta['name'],
                tiktok_nickname=author_meta['nickName'],
                tiktok_is_verified=author_meta['verified'],
                tiktok_signnature=author_meta['signature'],
                tiktok_avatar=author_meta['avatar'],
                tiktok_is_private_account=author_meta['privateAccount'],
            )

            author = await self.repository.save_author(author)
        else:
            author = await self.repository.update_author(
                author,
                tiktok_id=author_meta['id'],
                name=author_meta['name'],
                tiktok_display_name=author_meta['name'],
                tiktok_nickname=author_meta['nickName'],
                tiktok_is_verified=author_meta['verified'],
                tiktok_signnature=author_meta['signature'],
                tiktok_avatar=author_meta['avatar'],
                tiktok_is_private_account=author_meta['privateAccount'])

        if post is None:
            post = TikTokPostEntity(
                tiktok_id=post_data['id'],
                web_video_url=post_data['webVideoUrl'],
                digg_count=post_data['diggCount'],
                share_count=post_data['shareCount'],
                play_count=post_data['playCount'],
                comment_count=post_data['commentCount'],
                tiktok_location=post_data['locationCreated'],
                author_id=author.id, # PK to author
                video_id=video.id, # PK to video
                music_id=music.id, # PK to music
            )
            post = await self.repository.save_tiktok_post(post)
        else:
            post = await self.repository.update_tiktok_post(post)

    