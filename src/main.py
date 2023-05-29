from flask import Flask
from features.recommend_music.api import router as recommend_music_route
from di import init_di
from dotenv import load_dotenv

load_dotenv()
init_di()

app = Flask(__name__)

app.register_blueprint(recommend_music_route, url_prefix='/recommend-music/')

if __name__ == '__main__':
    app.run()