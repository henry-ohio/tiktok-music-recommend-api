
from flask import Blueprint, jsonify
from kink import inject
from features.recommend_music.use_cases.crawl_n_analyze_tiktok_data import UsecaseCrawlAndAnalyzeTikTokData

router = Blueprint('recommend-music', __name__)

@router.route('/analyze-tiktok', methods=['POST'])
@inject
def analyze_tiktok():
    uc = UsecaseCrawlAndAnalyzeTikTokData()
    result = uc.execute()
    return jsonify({
        'message': 'success'
    })

@router.route('/', methods=['GET'])
@inject
def get_music_recommendation():
    uc = UsecaseCrawlAndAnalyzeTikTokData()
    result = uc.execute()
    return jsonify({
        'message': 'success',
        'data': [
            # TODO list of recommended musics here
        ]
    })