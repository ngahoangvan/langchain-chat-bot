import sqlite3
from json.decoder import JSONDecodeError
from typing import Dict

import hishel
from httpx import HTTPStatusError
from httpx import Limits
from httpx import Timeout
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from core.constants import BASE_DIR
from core.decorators.processing_time import time_it
from core.loggers import configure_logging
from core.utils.common_utils import join_paths


logger = configure_logging(__name__)


class BaseAPIService:
    def __init__(self):
        self.storage = hishel.SQLiteStorage(
            connection=sqlite3.connect(
                join_paths(BASE_DIR, "hishel_cache.db"), timeout=5, check_same_thread=False,
            ),
        )
        self.controller = hishel.Controller(cacheable_methods=["GET", "POST"])
        self.client = hishel.CacheClient(
            controller=self.controller,
            limits=Limits(max_connections=1000),
            storage=self.storage,
            timeout=Timeout(timeout=300.0),
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=0, max=10))
    @time_it
    def get(self, endpoint, params: Dict = None, headers: Dict = None):
        logger.debug(f"Endpoint: {endpoint}, Method: GET")
        try:
            response = self.client.get(endpoint, params=params, headers=headers, timeout=Timeout(timeout=60.0))
            response.raise_for_status()
            try:
                data = response.json()
            except JSONDecodeError:
                data = response.text
            return data
        except HTTPStatusError as e:
            logger.error(f"Error: {e}")
            raise e

    async def aget(self, endpoint, params: Dict = None, headers: Dict = None):
        with hishel.AsyncCacheClient(
            controller=self.controller,
            limits=Limits(max_connections=1000),
            storage=self.storage,
            timeout=Timeout(timeout=60.0),
        ) as async_client:
            logger.debug(f"Endpoint: {endpoint}, Method: GET")
            try:
                response = await async_client.get(endpoint, params=params, headers=headers)
                response.raise_for_status()
                try:
                    data = response.json()
                except JSONDecodeError:
                    data = response.text

                return data
            except HTTPStatusError as e:
                logger.error(f"Error: {e}")
                raise e

    def wrap_get_api(self, headers, endpoint, params: Dict = None, *args, **kwargs):
        return self.get(endpoint, params, headers, *args, **kwargs)

    @time_it
    def post(self, endpoint, data: Dict = None, json: Dict = None, params: Dict = None, headers: Dict = None):
        logger.debug(f"Endpoint: {endpoint}, Method: POST")
        try:
            response = self.client.post(endpoint, data=data, json=json, params=params, headers=headers)
            response.raise_for_status()
            try:
                data = response.json()
            except JSONDecodeError:
                data = response.text

            return data
        except HTTPStatusError as e:
            logger.error(f"Error: {e}")
            raise e

    async def apost(self, endpoint, data: Dict = None, json: Dict = None, params: Dict = None, headers: Dict = None):
        with hishel.AsyncCacheClient(
            controller=self.controller,
            limits=Limits(max_connections=1000),
            storage=self.storage,
            timeout=Timeout(timeout=300.0),
        ) as async_client:
            logger.debug(f"Endpoint: {endpoint}, Method: POST")
            try:
                response = await async_client.apost(endpoint, data=data, json=json, params=params, headers=headers)
                response.raise_for_status()
                try:
                    data = response.json()
                except JSONDecodeError:
                    data = response.text

                return data
            except HTTPStatusError as e:
                logger.error(f"Error: {e}")
                raise e

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def put(self, endpoint, data: Dict = None, json: Dict = None, params: Dict = None, headers: Dict = None):
        logger.debug(f"Endpoint: {endpoint}, Method: PUT")
        try:
            response = self.client.put(endpoint, data=data, json=json, params=params, headers=headers)
            response.raise_for_status()
            try:
                data = response.json()
            except JSONDecodeError:
                data = response.text

            return data
        except HTTPStatusError as e:
            logger.error(f"Error: {e}")
            raise e

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def patch(self, endpoint, data: Dict = None, json: Dict = None, params: Dict = None, headers: Dict = None):
        logger.debug(f"Endpoint: {endpoint}, Method: PATCH")
        try:
            response = self.client.patch(endpoint, data=data, json=json, params=params, headers=headers)
            response.raise_for_status()
            try:
                data = response.json()
            except JSONDecodeError:
                data = response.text

            return data
        except HTTPStatusError as e:
            logger.error(f"Error: {e}")
            raise e

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def delete(self, endpoint, params: Dict = None, headers: Dict = None):
        logger.debug(f"Endpoint: {endpoint}, Method: DELETE")
        try:
            response = self.client.delete(endpoint, params=params, headers=headers)
            response.raise_for_status()
            try:
                data = response.json()
            except JSONDecodeError:
                data = response.text

            return data
        except HTTPStatusError as e:
            logger.error(f"Error: {e}")
            raise e

    async def adelete(self, endpoint, params: Dict = None, headers: Dict = None):
        with hishel.AsyncCacheClient(
            controller=self.controller,
            limits=Limits(max_connections=1000),
            storage=self.storage,
            timeout=Timeout(timeout=300.0),
        ) as async_client:
            logger.debug(f"Endpoint: {endpoint}, Method: DELETE")
            try:
                response = await async_client.delete(endpoint, params=params, headers=headers)
                response.raise_for_status()
                try:
                    data = response.json()
                except JSONDecodeError:
                    data = response.text

                return data
            except HTTPStatusError as e:
                logger.error(f"Error: {e}")
                raise e
