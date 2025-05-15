import os
from google.cloud import vision

# 初始化
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vision-api-key.json"
client = vision.ImageAnnotatorClient()

def recognize_food(image_bytes):
    image = vision.Image(content=image_bytes)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    if labels:
        return labels[0].description
    return None

def get_recipe(food_name):
    recipes = {
        "pizza": "1. 準備麵團\n2. 加入番茄醬和起司\n3. 放進烤箱烤約15分鐘",
        "hamburger": "1. 準備漢堡麵包\n2. 煎牛肉餅\n3. 組合：麵包 + 牛肉餅 + 生菜 + 番茄"
    }
    return recipes.get(food_name.lower(), "找不到此食物的製作過程，請嘗試其他食物。")
