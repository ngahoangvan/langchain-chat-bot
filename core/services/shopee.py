from core.loggers import configure_logging
from core.services.base_api import BaseAPIService
from core.utils.common_utils import join_paths

logger = configure_logging(__name__)


class ShopeeAPIService(BaseAPIService):
    def __init__(self):
        super().__init__()
        self.shopee_api_url = "https://gappapi.deliverynow.vn/"
        self.city_id = 219 # Da Nang

    @property
    def headers(self):
        return {
            'X-Foody-Access-Token': '',
            'X-Foody-Api-Version': '1',
            'X-Foody-App-Type': '1004',
            'X-Foody-Client-Id': '',
            'X-Foody-Client-Language': 'vi',
            'X-Foody-Client-Type': '1',
            'X-Foody-Client-Version': '3.0.0',
            'Content-Type': 'application/json'
        }

    def get_ids(self):
        response = self.post(
            endpoint=join_paths(self.shopee_api_url, "api/promotion/get_ids"),
            headers=self.headers,
            json={
                "city_id": self.city_id,
                "foody_service_id": 1,
                "promotion_status": 1,
                "sort_type": 0
            }
        )
        ids = response['reply']['promotion_ids']
        return ids

    def get_restaurant_infos(self):
        promotion_ids = self.get_ids()
        response = self.post(
            endpoint=join_paths(self.shopee_api_url, "api/promotion/get_infos"),
            headers=self.headers,
            json={
                "promotion_ids": promotion_ids,
            }
        )
        data = response['reply']['promotion_infos']
        return data
