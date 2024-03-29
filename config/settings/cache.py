from config.env import env

REDIS_URI = env("REDIS_URI", default="127.0.0.1:6379")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_URI}/cache",
    }
}
