# shopee_task.py

from celery import Task
from fastapi import Depends
from sqlalchemy.orm import Session

from core.databases.db import get_db
from core.databases.models.shopee import (LabelPhoto, Operating,
                                          PromotionGroup, Rating, Restaurant,
                                          ShippingMethod)
from core.services.shopee import ShopeeAPIService
from core.loggers import configure_logging


logger = configure_logging(__name__)


class ShopeeTask(Task):
    name = 'shopee_task'

    def __init__(self, service: ShopeeAPIService, db: Session = Depends(get_db)) -> None:
        super().__init__()
        self.service = service
        self.db = db
    
    def crawl(self, *args, **kwargs):
        restaurants = self.fetch_shopee_api_data()
        data = [
            dict(
                id=info['restaurant_info']['id'],
                name=info['restaurant_info']['name'],
                total_order=info['restaurant_info']['total_order'],
                city_id=info['restaurant_info']['city_id'],
                restaurant_id=info['restaurant_info']['restaurant_id'],
                restaurant_url=info['restaurant_info']['restaurant_url'],
                logo_mms_img_id=info['restaurant_info']['logo_mms_img_id'],
                brand_id=info['restaurant_info']['brand_id'],
                is_open=info['restaurant_info']['is_open'],
                contract_type=info['restaurant_info']['contract_type'],
                location_url=info['restaurant_info']['location_url'],
                has_contract=info['restaurant_info']['has_contract'],
                is_quality_merchant=info['restaurant_info']['is_quality_merchant'],
                merchant_time=info['restaurant_info']['merchant_time'],
                service_type=info['restaurant_info']['service_type'],
                url_rewrite_name=info['restaurant_info']['url_rewrite_name'],
                is_foody_delivery=info['restaurant_info']['is_foody_delivery'],
                address=info['restaurant_info']['address'],
                foody_service_id=info['restaurant_info']['foody_service_id'],
                url=info['restaurant_info']['url'],
                display_order=info['restaurant_info']['display_order'],
                delivery_id=info['restaurant_info']['delivery_id'],
                is_pickup=info['restaurant_info']['is_pickup'],
                banner_mms_img_id=info['restaurant_info']['banner_mms_img_id'],
                latitude=info['restaurant_info']['position']['latitude'],
                longitude=info['restaurant_info']['position']['longitude'],
                is_verified=info['restaurant_info']['position']['is_verified'],
                district_id=info['restaurant_info']['district_id'],
                limit_distance=info['restaurant_info']['limit_distance'],
                restaurant_status=info['restaurant_info']['restaurant_status'],
                image_name=info['restaurant_info']['image_name'],
            ) for info in restaurants
        ]
        self.db.bulk_insert_mappings(Restaurant, data)
        return {"status": "success", "data": "Shopee data crawled"}


    def fetch_shopee_api_data(self):
        restaurant_infos = self.service.get_restaurant_infos()
        return restaurant_infos

    def run(self, *args, **kwargs):
        return self.crawl(*args, **kwargs)
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"Task {task_id} succeeded with result: {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Task {task_id} failed with exception: {exc}")
        return super().on_failure(exc, task_id, args, kwargs, einfo)
