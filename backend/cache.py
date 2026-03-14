from datetime import datetime, timedelta

cache = {}
CACHE_TTL = timedelta(minutes=5)

def get_cache(key: str):
    if key in cache:
        if datetime.now() < cache[key]["expires_at"]:
            return cache[key]["data"]
        del cache[key]
    return None

def set_cache(key: str, data):
    cache[key] = {
        "data": data,
        "expires_at": datetime.now() + CACHE_TTL
    }

def invalidate_cache(ticker: str = None):
    """Invalida cache de um ticker específico ou todo o cache."""
    if ticker:
        keys_to_delete = [k for k in cache if ticker in k]
        for k in keys_to_delete:
            del cache[k]
    else:
        cache.clear()