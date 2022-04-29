import boto3

# Amazon Translate の client インスタンスを作成する
translate = boto3.client('translate')

# 英語に翻訳 元の言語は自動判定
def translate_to_english(input_text):
    response = translate.translate_text(
        Text = input_text,
        SourceLanguageCode = 'auto',
        TargetLanguageCode = 'en'
    )
    output_text = response.get('TranslatedText')
    return output_text