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
                en_list.append(temp_list[0])
                sy_list.append('null')
                temp_zh_word = '';
                for j in temp_list[1:]:
                    temp_zh_word += j
                zh_list.append(temp_zh_word)
        else:
            en_list.append(temp_list[0])
            sy_list.append(temp_list[1])
            if len(temp_list) > 3:
                temp_zh_word = '';
                for j in temp_list[2:]:
                    temp_zh_word += j
                zh_list.append(temp_zh_word)
            else:
                zh_list.append(temp_list[2])
    print(en_list)

get_word_list('F')