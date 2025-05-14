from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from linebot.exceptions import InvalidSignatureError

from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from google_api.places import search_restaurants
from google_api.directions import get_route

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text.strip()

    if user_input.startswith("路線 "):
        try:
            _, origin, destination = user_input.split()
            route_info = get_route(origin, destination)
            reply_text = f"🗺 **從 {origin} 到 {destination} 的建議路線**\n{route_info}"
        except:
            reply_text = "❌ 請輸入格式：**路線 出發地 目的地**"
        messages = [reply_text]

    elif len(user_input) >= 2:
        messages = search_restaurants(user_input)
    else:
        messages = ["❌ 請輸入 **城市名稱 + 美食類型**（例如：「臺北燒肉」），或使用 路線 出發地 目的地 查詢路線。"]

    first_message_sent = False
    for msg in messages:
        if msg.startswith("http"):
            line_bot_api.push_message(
                event.source.user_id,
                ImageSendMessage(original_content_url=msg, preview_image_url=msg)
            )
        else:
            text_message = TextSendMessage(text=msg)
            if not first_message_sent:
                line_bot_api.reply_message(event.reply_token, text_message)
                first_message_sent = True
            else:
                line_bot_api.push_message(event.source.user_id, text_message)

def setup_webhook(app):
    @app.route("/callback", methods=["POST"])
    def callback():
        signature = request.headers.get("X-Line-Signature", "")
        body = request.get_data(as_text=True)
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return "OK"