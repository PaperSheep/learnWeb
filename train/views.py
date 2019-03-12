from django.shortcuts import render_to_response, get_object_or_404, redirect, render, HttpResponse
from .models import WordDbType, Word, UserWord
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import django.utils.timezone as timezone
from django.http import JsonResponse  # 返回json格式数据



@login_required(login_url='home')
def review_page(request, word_type_pk):
    word_type = get_object_or_404(WordDbType, pk=word_type_pk)
    # user_words = UserWord.objects.filter(player=request.user, english__word_db_type=word_type).order_by('mastery_level')  # 外键属性的筛选
    user_words = UserWord.objects.filter(player=request.user, english__word_db_type=word_type)
    if len(user_words) == 0:
        return redirect('band_with_type', word_type.pk)
    for word in user_words:
        # word.review_time = word.review_time.replace(tzinfo=None)  # 清空时区信息
        delta_hours = round((timezone.now() - word.review_time).total_seconds() / 3600, 2)
        # 复习次数小于五次执行遗忘曲线
        if delta_hours > 1 and word.review_count < 5:
            word.mastery_level /= delta_hours  # 遗忘曲线
            word.review_time = timezone.now()
            word.save()
    user_words = UserWord.objects.filter(player=request.user, english__word_db_type=word_type).order_by('mastery_level')

    context = {}
    context['word_type'] = word_type
    context['words'] = user_words[:10]
    context['word_pk'] = []
    for word in context['words']:
        context['word_pk'].append(word.pk)
    # return render_to_response('train/review_page.html', context)
    return render(request, 'train/review_page.html', context)

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
    context['english'] = []
    context['chinese'] = []
    context['word_pk'] = []
    context['words'] = word_list
    context['word_type'] = word_type
    for word in context['words']:
        context['english'].append(word.english)
        context['chinese'].append(word.chinese)
        context['word_pk'].append(word.pk)

    return render(request, 'train/eng.html', context)

@login_required(login_url='home')
def level_tow(request):
    print(1)
    try:
        word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])

        context = {}
        # print(request.POST['en_word'])
        context['english'] = request.POST['en_word'].split(',')
        context['chinese'] = request.POST['zh_word'].split(',')
        context['word_pk'] = request.POST['word_pk'].split(',')
        context['word_type'] = word_type
        # return render_to_response('train/level_tow.html', context)
        print(2)
        return render(request, 'train/level_tow.html', context)
    except:
        print(3)
        return redirect('home')
    print(4)

@login_required(login_url='home')
def exam(request, word_type_pk):
    word_type = get_object_or_404(WordDbType, pk=word_type_pk)
    user_db_word = list(UserWord.objects.filter(player=request.user, english__word_db_type=word_type))
    context = {}

    words = []
    context['english'] = []
    context['chinese'] = []
    context['word_pk'] = []
    for i in range(0, 10):
        words.append(random.choice(user_db_word))
        user_db_word.remove(words[i])
    for word in words:
        context['english'].append(word.english.english)
        context['chinese'].append(word.english.chinese)
        context['word_pk'].append(word.pk)
    context['word_type'] = word_type
    # return render_to_response('train/exam.html', context)
    return render(request, 'train/exam.html', context)

@login_required(login_url='home')
def level_three(request):
    try:
        word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])

        context = {}
        context['english'] = request.POST['en_word'].split(',')
        context['chinese'] = request.POST['zh_word'].split(',')
        context['word_pk'] = request.POST['word_pk'].split(',')
        context['word_type'] = word_type
        # print(context['english'])
        # print(context['chinese'])
        # return render_to_response('train/level_three.html', context)
        return render(request, 'train/level_three.html', context)
    except:
        return redirect('home')

# 学习完之后的存储数据
@login_required(login_url='home')
def finished(request):
    word_pk_list = request.POST['word_pk'].split(',')
    word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])
    user_db_word = UserWord.objects.filter(player=request.user, english__pk__in=word_pk_list)
    # 排除重复提交表单
    if len(user_db_word) == 0:
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
    deviation_list = request.POST['deviation_list'].split(',')
    is_tip_list = request.POST['is_tip'].split(',')
    # data_tup = (word_pk_list, deviation_list, is_tip_list)

    word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])
    for i, word_pk in enumerate(word_pk_list):
        user_word = UserWord.objects.get(pk=int(word_pk))
        if is_tip_list[i] == 'true':
            user_word.mastery_level -= 10
        else:
            is_positive = int(deviation_list[i])
            if is_positive > 0:
                user_word.review_count += 1
            user_word.mastery_level += is_positive
            # 掌握值界限[0，100]
            if user_word.mastery_level < 0:
                user_word.mastery_level = 0
            elif user_word.mastery_level > 100:
                user_word.mastery_level = 100
        user_word.review_time = timezone.now()  # 更新单词复习时间
        user_word.save()
    return redirect('band_with_type', word_type.pk)

# 测验完之后更新存储数据
@login_required(login_url='home')
def exam_finished(request):
    word_pk_list = request.POST['word_pk'].split(',')
    true_list = request.POST['true_list'].split(',')
    word_type = get_object_or_404(WordDbType, type_name=request.POST['word_type'])
    for i, value in enumerate(true_list):
        user_word = UserWord.objects.get(pk=int(word_pk_list[i]))
        if value == 'true':
            user_word.mastery_level += 5
            user_word.review_time = timezone.now()  # 更新单词复习时间
        else:
            user_word.mastery_level -= 5
        # 掌握值界限[0，100]
        if user_word.mastery_level < 0:
            user_word.mastery_level = 0
        elif user_word.mastery_level > 100:
            user_word.mastery_level = 100
        user_word.save()

    return redirect('band_with_type', word_type.pk)


def upload_file(request):
    # print("FILES:", request.FILES)
    # print("POST:", request.POST)
    # print(request.POST['1'])
    # print(request.POST['2'])
    # print(type(request.POST['2']))
    # return HttpResponse("上传成功!")
    context = {
                "data1": Word.objects.all()[0].chinese,
               "data2": Word.objects.all()[0].english,
   }
    return JsonResponse(context)

def test(request):
    return render(request, 'train/test.html')
