# TikTok Music Recommendation Test

This is source code for TikTok Music Recommendation testing assignment.

## Techstack used

- Python 3.10
- Flask
- SQLAlchemy + Alembic
- PostgreSQL
- Docker

## Set up and run localhost

1. Run `docker compose up -d` to start database service. Wait for a few minutes for it to get ready.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
alembic --raiseerr -c src/alembic.ini upgrade head 
alembic --raiseerr -c src/alembic.ini stamp head 
```

4. Start server

```bash
python src/main.py
```

## Code specification

- Use Clean Architecture + Vertical Slice Architecture.
- Use Dependencies Injection with Kink

## Code architecture

- The app is divided to multiple features, each contain inside one folder in `features` directory.
- Each feature folder has 3 subfolders:
    - `domain`: Contains entities definitions and core business logic, like the recommendation algorithm.
    - `data`: Contains data access logics and models, like Repositories, DAO, ORM.
    - `api` (a.k.a presentation layer): Handle API request (using Flask framework), schema check, data validation, authentication, role checking...
    Flow: `User Request` -> `API layer` -> `Domain layer` -> `Data layer`
- Outside there are shared folders for all features:
    - `core`: Define common modules that can be used for all features.
    - `base`: Define base classes.
    - `utils`: Utility functions.
    - `config`: Configuration class.
- App start at `main.py` file.
- `di.py` file define the Dependencies.

# Tasks requirements

Music Recommendation for TikTok videos.

1. **Analyzing Influencer Profile**: Develop a simple method to extract relevant information from the influencer's profile that can be used for recommendation purposes. Consider factors such as **follower count**, **view**, **like**, **share count** for videos and any other basic attributes. *Implementing scraper is outside of the scope of this task* so you are allowed to use mock data for this particular subtask. Imagine you already have a scraper solution in place which can provide you all that data. For your reference, we provide sample scrape result in the attachment.
2. **Content Analysis**: Implement a basic mechanism to analyze the influencer's TikTok videos to **understand their content patterns and preferences**. Extract information from the video itself to determine factors such as **genre**, **mood**, **tempo**, and any other relevant attributes. Additionally, you can assume that you have access to video metadata such as information above (count, view, like, share count, music used and etc, however the video content itself is yet to be analyzed which is the essence of this subtask)
3. **Music Analysis**: Incorporate music analysis into the recommendation process. You can either analyze the music tracks directly or use information obtained from a music API (e.g., Spotify API) to retrieve attributes such as genre, mood, tempo, popularity, and any other relevant factors.
4. **Recommendation Engine**: Build a recommendation engine that takes into account the influencer's profile information, content analysis results, and music analysis results to suggest suitable music options. Consider factors like genre, mood, tempo, popularity, and any other relevant attributes for generating recommendations.


## Database design

My idea here is that entities like `Author`, `Video` and `Music` are the core entities, which can existing in multiple platforms. For example, one `Music` song can be presented on TikTok, Spotify, and Youtube. Sometimes we can catch early trends on Spotify then recommend on TikTok.

Therefore in this design, I only have 3 tables: `Author`, `Video` and `Music`. Each of them can have one or multiple sources, and related to each other just like how we normally see them in the real world:

- An `Author` can have multiple `Music` and `Video` owned by them.
- A `Video` can use one or multiple `Music`s.
- A `Video` or `Music` can be published on one or multiple platforms.

> I haven't think much about the exact mechanism on how we can merge the same videos or musics on different platforms into one single entity, but I know it's possible.

> This is just a quick design and I'm aware that I haven't covered complex cases yet. For example, I don't handle case 1 video is posted multiple times using different accounts.

### ERD:

TODO

- Table **author**: General info for the Author, include name, description,... and platform specific attributes. E.g, TikTok profile: `id`, `name`, `signature`...
- Table **music**, **video**: name, link, data, and platform data (I use simple JSON for now, but it should be separated tables for each provider).

## Flow

1. An App or a cron job calls API `/analyze-tiktok` -> Back-end call Tiktok API (mock) and:
    - Record authors, musics and videos to database
    - Do some analyze on `music` for follow genre, mood, tempo, popularity.
    - Do some analyze on `author` for follower count, view, like, share count,...
    
2. User call API `/recommend-music` to get the recommended music. 

> Note that for now I only recommend based on max attribute count.

# Database Migration

## Create migration

## Migration database

To create migration, run:
  
```bash
alembic --raiseerr -c src/alembic.ini revision --autogenerate -m "message"
```

## Apply migration

- Upgrade
  
```bash
alembic --raiseerr -c src/alembic.ini upgrade head 

alembic --raiseerr -c src/alembic.ini stamp head 
```

- Downgrade

```bash
cd src

alembic --raiseerr -c src/alembic.ini downgrade -1

alembic --raiseerr -c src/alembic.ini stamp head
```