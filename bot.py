#!/usr/bin/python3.8
from googletrans import Translator

translator = Translator()
test = []
translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
for translation in translations:
    test.append(translation.text)
    print(translation.origin, ' -> ', translation.text)
print(test)
translation_rev = translator.translate(test, dest='en')
for translation in translation_rev:
    print(translation.text)
print(translator.translate('veritas lux mea', src='la').text)
