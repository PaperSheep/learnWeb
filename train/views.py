from django.shortcuts import render_to_response, get_object_or_404, redirect
from .models import WordDbType, Word, UserDbWord
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import json

@login_required(login_url='home')
def word_train(request, first_letter, word_type_type_name):
    # 返回随机的十个单词
    word_type = get_object_or_404(WordDbType, type_name=word_type_type_name)
    first_letter_list = list(Word.objects.filter(first_letter=first_letter, word_db_type=word_type))
    word_list = []
    for i in range(0, 10):
        word_list.append(first_letter_list.pop(random.choice(range(0, len(first_letter_list)))))

    context = {}
    # context['words'] = Word.objects.all()[:10]
    context['english'] = []
    context['chinese'] = []
    context['words'] = word_list
    context['word_type'] = word_type
    for word in context['words']:
        context['english'].append(word.english)
        context['chinese'].append(word.chinese)
    return render_to_response('train/eng.html', context)

@login_required(login_url='home')
def level_tow(request):
    context = {}
    context['english'] = request.POST['en_word'].split(',')
    context['chinese'] = request.POST['zh_word'].split(',')
    context['word_type'] = request.POST['word_type']
    return render_to_response('train/level_tow.html', context)

@login_required(login_url='home')
def level_three(request):
    word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])

    context = {}
    context['english'] = request.POST['en_word'].split(',')
    context['chinese'] = request.POST['zh_word'].split(',')
    context['word_type'] = word_type
    # print(context['english'])
    # print(context['chinese'])
    return render_to_response('train/level_three.html', context)

def test_word(request):
    word_type = get_object_or_404(WordDbType, type_name='CET4')
    user = get_object_or_404(User, username='god')
    first_letter_list = Word.objects.filter(first_letter='A', word_db_type=word_type)
    user_words = UserDbWord.objects.filter(player=user)
    for word in user_words:
        if word.english in first_letter_list:
            print(word.english)

    context = {}
    # context['words'] = words['english']
    # print(context['words'])

    return render_to_response('train/test.html', context)
