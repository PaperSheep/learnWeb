# 处理单词文本
# 将单词文本预处理

word_list = []
alphbat = '计算机专业英语/all'
with open('word_band/{}_word.txt'.format(alphbat), 'r', encoding='UTF-8') as f:
    i = 1
    for line in f.readlines():
        # if i % 2 != 0:
        #     word_list.append(line.replace(u'\u3000',u'').replace('/ ','/'))
        # i += 1
        # line = line[line.find('.') + 1:]
        word_list.append(line.replace(' [', '/').replace('] ', '/'))

with open('word_band/{}_word.txt'.format(alphbat), 'w', encoding='UTF-8') as f:
    f.writelines(word_list)

print('应该成功吧')
