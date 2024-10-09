# from django.template.loader import get_template
# try:
#     template = get_template('generatorius/edit_text.html')
#     print("Template found!")
# except Exception as e:
#     print(f"Error: {e}")
from gtts.lang import tts_langs
print(tts_langs())