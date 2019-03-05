from django.shortcuts import render_to_response, get_object_or_404, redirect
from .models import WordDbType, Word, UserWord
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
# import json

def test(request):
    context = {}
    return render_to_response('view_completed.html', context)

@login_required(login_url='home')
def review_page(request, word_type_pk):
    word_type = get_object_or_404(WordDbType, pk=word_type_pk)
    user_words = UserWord.objects.filter(player=request.user, english__word_db_type=word_type).order_by('mastery_level')  # 外键属性的筛选

    context = {}
    context['word_type'] = word_type
    context['words'] = user_words[:10]
    context['word_pk'] = []
    for word in context['words']:
        context['word_pk'].append(word.pk)
    return render_to_response('train/review_page.html', context)

@login_required(login_url='home')
def word_train(request, first_letter, word_type_type_name):
    # 返回随机的十个单词
    word_type = get_object_or_404(WordDbType, type_name=word_type_type_name) 
    first_letter_list = list(Word.objects.filter(first_letter=first_letter, word_db_type=word_type))  # 获得塞选出来的单词表
    # user = get_object_or_404(User, username=request.user.username)
    user_words = list(UserWord.objects.filter(player=request.user, english__in=first_letter_list))  # 获得塞选出来的用户的单词表
    for word in user_words:
        if word.english in first_letter_list:
            first_letter_list.remove(word.english)
    word_count = len(first_letter_list)
    word_list = []
    if word_count > 10:
        for i in range(0, 10):
            word_list.append(first_letter_list.pop(random.choice(range(0, len(first_letter_list)))))
    elif word_count > 0:
        word_list = first_letter_list  # 小于或等于10个直接取单词数组
    else:
        # 该首字母头的词已经学完
        return redirect('band_with_type', word_type.pk)

    context = {}
    # context['words'] = Word.objects.all()[:10]
    context['english'] = []
    context['chinese'] = []
    context['word_pk'] = []
    context['words'] = word_list
    context['word_type'] = word_type
    for word in context['words']:
        context['english'].append(word.english)
        context['chinese'].append(word.chinese)
        context['word_pk'].append(word.pk)
    # print(context['english'])
    return render_to_response('train/eng.html', context)

@login_required(login_url='home')
def level_tow(request):
    word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])

    context = {}
    # print(request.POST['en_word'])
    context['english'] = request.POST['en_word'].split(',')
    context['chinese'] = request.POST['zh_word'].split(',')
    context['word_pk'] = request.POST['word_pk'].split(',')
    context['word_type'] = word_type
    return render_to_response('train/level_tow.html', context)

@login_required(login_url='home')
def level_three(request):
    word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])

    context = {}
    context['english'] = request.POST['en_word'].split(',')
    context['chinese'] = request.POST['zh_word'].split(',')
    context['word_pk'] = request.POST['word_pk'].split(',')
    context['word_type'] = word_type
    # print(context['english'])
    # print(context['chinese'])
    return render_to_response('train/level_three.html', context)

# 学习完之后的存储数据
@login_required(login_url='home')
def finished(request):
    word_pk_list = request.POST['word_pk'].split(',')
    word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])
    for word_pk in word_pk_list:
        word_model = get_object_or_404(Word, pk=int(word_pk))
        new_word = UserWord()
        new_word.player = request.user
        new_word.english = word_model
        new_word.save()
    return redirect('band_with_type', word_type.pk)

# 复习完之后更新存储数据
@login_required(login_url='home')
def review_finished(request):
    word_pk_list = request.POST['word_pk'].split(',')
    word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])
    for word_pk in word_pk_list:
        user_word = UserWord.objects.get(pk=int(word_pk))
        user_word.mastery_level += 5
        user_word.save()
    return redirect('band_with_type', word_type.pk)
