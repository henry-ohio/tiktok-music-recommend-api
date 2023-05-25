from flask import Flask
from features.recommend_music.api import routes

app = Flask(__name__)

if __name__ == '__main__':
    app.run()