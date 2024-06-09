import deepl
from django.conf import settings

# 요약 내용을 지정된 언어로 번역
def translate_summary(content, language):
    auth_key = settings.DEEPL_API_KEY
    translator = deepl.Translator(auth_key)

    if isinstance(content, dict):  # content가 dict 형태일 때, 각 값을 번역
        translated_data = {}
        for key, value in content.items():
            result = translator.translate_text(value, target_lang=language)
            translated_data[key] = result.text
        return translated_data
    elif isinstance(content, str):  # content가 문자열일 때, 직접 번역
        result = translator.translate_text(content, target_lang=language)
        return result.text