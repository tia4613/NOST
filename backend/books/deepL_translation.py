import deepl
from django.conf import settings

# 요약 내용 지정 언어로 번역
def translate_summary(content, language) :
    
    auth_key = settings.DEEPL_API_KEY
    translator = deepl.Translator(auth_key)
    if isinstance(content,dict) : #data 값이 dict 형태일때 번역
        translated_data = {}
        for key,value in content.items() :
            result = translator.translate_text(value, target_lang=language)
            translated_data[key] = result.text
        return translated_data
    elif isinstance(content,str) : #data 값이 text 형태일때 번역
        result = translator.translate_text(content, target_lang=language)
        return result.text
