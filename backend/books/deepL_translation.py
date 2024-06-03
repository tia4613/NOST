import deepl
from django.conf import settings

# 요약 내용 지정 언어로 번역
def translate_summary(summary, language) :
    
    auth_key = settings.DEEPL_API_KEY
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(summary, target_lang=language)
    return result