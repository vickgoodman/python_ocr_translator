# translator.py

from googletrans import Translator
translator = Translator()

def translate_text(text, dest_lang='ro'):
    return translator.translate(text, dest=dest_lang).text
