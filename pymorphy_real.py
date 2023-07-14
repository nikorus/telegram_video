'''
Это код из обсуждений видео - улучшае обработку мата
'''

import pymorphy2
import string

# так в Python создается обычная функция
def normal_mat(word: str):
    # в этом месте проводятся операции как в видео
    word = word.lower().translate(str.maketrans('', '', string.punctuation))
    # здесь создается переменная класса. она нужна, чтобы спарсить слово в следующей строке
    morph = pymorphy2.MorphAnalyzer()
    """
    вот такой ответ будет на примере слова "дураки"
    [Parse(word='дураки', tag=OpencorporaTag('NOUN,anim,masc plur,nomn'), normal_form='дурак', score=1.0, methods_stack=((DictionaryAnalyzer(), 'дураки', 2, 6),))]
    {'дурак'}
    """
    parsed_token = morph.parse(word)
    # выводится нормальная форма. normal_form см. выше
    normal_form = parsed_token[0].normal_form
    return normal_form

# и заменить часть кода в echo_send

# if {normal_mat(i) for i in message.text.split(' ')}
