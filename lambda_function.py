import os
import logging
from chalicelib import aws_functions
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)

# logger 設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# LINE Bot API 設定
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


def lambda_handler(event, context):
    if "x-line-signature" in event["headers"]:
        signature = event["headers"]["x-line-signature"]
    elif "X-Line-Signature" in event["headers"]:
        signature = event["headers"]["x-line-signature"]
    # リクエストボディを取得
    body = event["body"]
    ok_json = {"isBase64Encoded": False,
               "statusCode": 200,
               "headers": {},
               "body": ""}
    error_json = {"isBase64Encoded": False,
                  "statusCode": 500,
                  "headers": {},
                  "body": "Error"}
    # メッセージイベント

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        logger.info('CALLED: handle_message()')

        # get message.text
        received_text = event.message.text
        logger.info(f'RECEIVED_TEXT: {received_text}')

        # Execute translation function
        translated_text = aws_functions.translate_to_english(received_text)
        logger.info(f'TRANSLATED_TEXT: {translated_text}')

        # Reply message
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=TextSendMessage(text=translated_text)
        )

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        logger.error(
            "Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            logger.error("  %s: %s" % (m.property, m.message))
        return error_json
    except InvalidSignatureError:
        return error_json
    return ok_json
