from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 從環境變數取得 LINE Channel 資訊
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("GYPjie6YaWO7MdbozUkLJYy0hkn3sltjpDxrLXhZkGgWDg6EGoShzaT4TV9CltprV0I/AtoooYaiiaqo7rfNnQ5NIEYbCQsStVOw++/SpzMUP9Y27v/PTATaGujenDTVg1XsTy40HQTyTQ6pWko6aQdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("398345023b4120cff4f79adf0532a4c9")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你說了: {event.message.text}")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
