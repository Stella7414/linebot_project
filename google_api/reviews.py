import requests
from config import GOOGLE_PLACES_API_KEY

def get_reviews(place_id):
    review_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": GOOGLE_PLACES_API_KEY,
        "language": "zh-TW"
    }

    try:
        response = requests.get(review_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "result" in data and "reviews" in data["result"]:
            reviews = data["result"]["reviews"]
            for review in reviews:
                if 'zh' in review['language']:
                    return review['text']
            return reviews[0]['text'] if reviews else None
        return None
    except requests.exceptions.RequestException:
        return None