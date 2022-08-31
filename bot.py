#!/usr/bin/python3.8
import os
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()

# Translation Testing
translator = Translator()
test = []
# Translation via lists
translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
for translation in translations:
    test.append(translation.text)
    print(translation.origin, ' -> ', translation.text)
print(test)
# Testing translating back to original language
translation_rev = translator.translate(test, dest='en')
for translation in translation_rev:
    print(translation.text)
# Testing single string translation
print(translator.translate('veritas lux mea', src='la').text)
