# 录入数据
# 把单词批量存进数据库

from train.models import WordDbType, Word
# import re
# from django.contrib.auth.models import User
# user = User.objects.all()[0] 


def get_word_list(alphbat):
    word_list = []
    with open('{}_word.txt'.format(alphbat), 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            word_list.append(line.replace('\n', ''))
        # word_list = f.readlines()
    # print(word_list[:5])
    en_list = []
    sy_list = []
    zh_list = []
    for i in word_list:
        temp_list = i.split('/')
        if len(temp_list) < 3:
            temp_list = i.split(' ')
            if temp_list[0].count('.') <= 0:
                en_list.append(temp_list[0].replace(' ', ''))
                sy_list.append('null')
                temp_zh_word = '';
                for j in temp_list[1:]:
                    temp_zh_word += j
                zh_list.append(temp_zh_word)
        else:
            en_list.append(temp_list[0].replace(' ', ''))
            sy_list.append(temp_list[1])
            if len(temp_list) > 3:
                temp_zh_word = '';
                for j in temp_list[2:]:
                    temp_zh_word += j
                zh_list.append(temp_zh_word)
            else:
                zh_list.append(temp_list[2])
            

    return en_list, sy_list, zh_list


def do_it(alphbat):
    word_type = WordDbType.objects.all()[0]
    en_list = []
    sy_list = []
    zh_list = []
    en_list, sy_list, zh_list = get_word_list(alphbat)
    i = 0
    for en_word in en_list:
        new_word = Word()
        new_word.word_db_type = word_type
        new_word.first_letter = alphbat
        new_word.english = en_word
        new_word.phonetic_symbol = sy_list[i]
        new_word.chinese = zh_list[i]
        new_word.save()
        i += 1
    print('应该成功吧')

# 改数据
# from train.models import Word
# a = Word.objects.get(chinese='xxx')
# a.english = 'boil'
# a.save()

# 清理数据库单词里的空格
def clear_words_space():
    all_word = Word.objects.all()
    for word in all_word:
        if ' ' in word.english:
            temp_en = word.english
            print(temp_en)
            a = Word.objects.get(english=temp_en)
            a.english = temp_en.replace(' ', '')
            a.save()
    print('清理结束，应该成功的吧')
