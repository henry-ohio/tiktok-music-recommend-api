from kink import inject
from ..data import RecommendMusicRepository

@inject
class BaseRecommendMusicUsecase:
    def __init__(self, repository: RecommendMusicRepository):
        self.repository = repository