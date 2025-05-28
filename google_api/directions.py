import re
import requests
from config import GOOGLE_MAPS_API_KEY

def get_route(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "walking",
        "language": "zh-TW",
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK":
            steps = data["routes"][0]["legs"][0]["steps"]
            directions = "\n".join([
                f"{i+1}. {re.sub('<[^<]+?>', '', step['html_instructions'])}"
                for i, step in enumerate(steps)
            ])
            map_link = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=walking"
            directions += f"\n\n📍 點我直接導航：\n👉 {map_link}"
            return directions
        else:
            return "🚫 無法取得路線，請確認地點是否正確。"
    except requests.exceptions.RequestException as e:
        return f"❌ 查詢路線時發生錯誤：{e}"
