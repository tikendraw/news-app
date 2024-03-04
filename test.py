import urllib.parse

params = {
    "category": "health",
    "lang": None,
    "country": "ind",
    "max": "33",
    "apikey": "lkasdf",
}
encoded_params = urllib.parse.urlencode(params)
a = f"https://gnews.io/api/v4/top-headlines?{encoded_params}"

print(a)
