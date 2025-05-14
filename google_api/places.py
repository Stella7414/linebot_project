import requests
from config import GOOGLE_PLACES_API_KEY
from google_api.reviews import get_reviews

def search_restaurants(location):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{location} 餐廳",
        "key": GOOGLE_PLACES_API_KEY,
        "language": "zh-TW",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "results" not in data or not data["results"]:
            return ["😢 沒有找到相關餐廳，請換個關鍵字試試看！"]

        restaurants = sorted(data["results"], key=lambda r: r.get("rating", 0), reverse=True)[:3]
        messages = ["🍽 **熱門餐廳推薦** 🍽\n"]

        for index, r in enumerate(restaurants, start=1):
            name = r.get("name", "未知餐廳")
            rating = r.get("rating", "無評分")
            address = r.get("formatted_address", "無地址資訊")
            business_status = r.get("business_status", "無營業資訊")
            place_id = r.get("place_id", "")

            photo_url = None
            if "photos" in r:
                photo_reference = r["photos"][0]["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"

            reviews = get_reviews(place_id)

            message = f"🏆 **{index}. {name}**\n"
            message += f"⭐ 評分：{rating}/5.0\n"
            message += f"📍 地址：{address}\n"
            message += f"🕒 營業狀況：{business_status}\n"
            if reviews:
                message += f"💬 最佳評論：{reviews}\n"
            message += f"🚗 [Google Maps 導航](https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')})\n"

            messages.append(message.strip())

            if photo_url:
                messages.append(photo_url)

        return messages

    except requests.exceptions.RequestException as e:
        return [f"❌ 無法獲取餐廳資訊：{e}"]