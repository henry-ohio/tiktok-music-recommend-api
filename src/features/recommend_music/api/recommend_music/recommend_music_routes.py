
from flask import Blueprint, jsonify, request
from kink import inject
from dataclasses import asdict
from features.recommend_music.use_cases.crawl_n_analyze_tiktok_data import UsecaseCrawlAndAnalyzeTikTokData
from features.recommend_music.use_cases.recommend_music import UsecaseRecommendMusic

router = Blueprint('recommend-music', __name__)

@router.route('/analyze-tiktok/', methods=['POST'])
def analyze_tiktok():
    uc = UsecaseCrawlAndAnalyzeTikTokData()
    result = uc.execute()
    return jsonify({
        'message': 'success'
    })

@router.route('/', methods=['GET'])
def get_music_recommendation():
    args = request.args
    skip = args.get('skip', 0)
    limit = args.get('limit', 5)

    uc = UsecaseRecommendMusic()
    result = uc.execute(skip=skip, limit=limit)

    return jsonify({
        'message': 'success',
        'data': [asdict(r) for r in result]
    })