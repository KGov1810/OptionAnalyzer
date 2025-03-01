class BaseExtractor:
    def __init__(self, base_url=None, headers=None):
        pass
    def _make_request(self, url, params=None):
        pass
    
class BarchartApi(BaseExtractor):
    def __init__(self):
        super().__init__()