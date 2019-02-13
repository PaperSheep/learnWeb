from django.shortcuts import render_to_response, get_object_or_404
from .models import WordDbType, Word
import random
import json

def word_train(request, first_letter):
    # 返回随机的十个单词
    first_letter_list = list(Word.objects.filter(first_letter=first_letter))
    word_list = []
    for i in range(0, 10):
        word_list.append(first_letter_list.pop(random.choice(range(0, len(first_letter_list)))))

    context = {}
    # context['words'] = Word.objects.all()[:10]
    context['english'] = []
    context['chinese'] = []
    context['words'] = word_list
    for word in context['words']:
        context['english'].append(word.english)
        context['chinese'].append(word.chinese)
    return render_to_response('train/eng.html', context)

def level_tow(request):
    context = {}
    context['english'] = request.POST['en_word'].split(',')
    context['chinese'] = request.POST['zh_word'].split(',')
    return render_to_response('train/level_tow.html', context)

def level_three(request):
    context = {}
    context['english'] = request.POST['en_word'].split(',')
    context['chinese'] = request.POST['zh_word'].split(',')
    # print(context['english'])
    # print(context['chinese'])
    return render_to_response('train/level_three.html', context)
