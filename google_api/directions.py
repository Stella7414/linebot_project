import re  # 匯入 re 模組，用來處理 HTML 格式指令的去除（例如 <b>、<div> 等標籤）
import requests  # 匯入 requests 模組，用來發送 HTTP 請求
from config import GOOGLE_MAPS_API_KEY  # 從 config 模組匯入 Google Maps API 金鑰

# 取得從 origin 到 destination 的步行路線指引
def get_route(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"  # Google Maps Directions API 的網址
    params = {
        "origin": origin,  # 起點
        "destination": destination,  # 終點
        "mode": "walking",  # 查詢方式為步行
        "language": "zh-TW",  # 回傳語言為繁體中文
        "key": GOOGLE_MAPS_API_KEY  # API 金鑰
    }

    try:
        response = requests.get(url, params=params, timeout=10)  # 發送 GET 請求並設定 10 秒超時
        response.raise_for_status()  # 檢查是否有發生 HTTP 錯誤（例如 404、500）
        data = response.json()  # 將回應轉換為 JSON 格式

        if data["status"] == "OK":  # 確認回應成功
            steps = data["routes"][0]["legs"][0]["steps"]  # 取得步驟列表（導航指示）
            directions = "\n".join([  # 將每個步驟組成文字，每行為一個步驟
                f"{i+1}. {step['html_instructions'].replace('<b>', '').replace('</b>', '')}"# 移除 HTML 標籤，只保留純文字
                for i, step in enumerate(steps)  # 對每個步驟編號與處理
            ])
            # 產生一個 Google Maps 的導覽連結
            map_link = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=walking"
            directions += f"\n\n📍 點我直接導航：\n👉 {map_link}"  # 加上導航連結文字
            return directions  # 回傳組合好的路線指引
        else:
            return "🚫 無法取得路線，請確認地點是否正確。"  # API 回傳錯誤（例如地址無效）
    except requests.exceptions.RequestException as e:  # 捕捉 HTTP 請求中可能發生的錯誤
        return f"❌ 查詢路線時發生錯誤：{e}"  # 回傳錯誤訊息
