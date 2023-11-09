import redis

from flask import json
from project.config.development import REDIS_HOST,REDIS_PASSWORD,REDIS_PORT

try:
    redis_client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,  
        db=0  
    )
    if redis_client.ping():
        print("Connected to Redis successfully.")
    else:
        print("Could not connect to Redis. Please check your connection details.")

except redis.ConnectionError as e:
    print(f"Could not connect to Redis: {str(e)}")
    redis_client = None

def get_cached_data(cache_key):
    if redis_client:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return cached_data
    return None


def set_cached_data(cache_key, data, expiration_time=3600):
    if redis_client:
        
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        redis_client.setex(cache_key, expiration_time, json_data)