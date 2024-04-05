import json
from pathlib import Path

CACHE_FILE = Path(__file__).parent / "cache.json"

def load_cache():
    """Load the cache from the cache file."""
    try:
        with CACHE_FILE.open("r") as f:
            cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        cache = {}
    return cache

def save_cache(cache):
    """Save the cache to the cache file."""
    with CACHE_FILE.open("w") as f:
        json.dump(cache, f, indent=4)

def is_url_cached(url, cache):
    """Check if a URL is already cached."""
    return url in cache

def cache_url(url, cache):
    """Add a URL to the cache."""
    cache[url] = True