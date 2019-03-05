from django.shortcuts import render_to_response, get_object_or_404, redirect
from train.models import WordDbType, Word, UserWord
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# 返回列表数据
def list_data(word_type, context):
    first_letter_list = Word.objects.values('first_letter').distinct().order_by('first_letter')  # 去重，再排序
    percent_list = {}
    for letter in first_letter_list:
        word_list = Word.objects.filter(word_db_type=word_type, first_letter=letter['first_letter'])
        user_word = UserWord.objects.filter(player=context['user'], english__in=word_list)
        if word_list.count() != 0:
            percent_list[letter['first_letter']] = round(round(user_word.count() / word_list.count(), 2) * 100)
    context['percent_list'] = percent_list

# 默认主页
def home(request):
    word_db_type = WordDbType.objects.all()
    word_type = get_object_or_404(WordDbType, pk=1)

    context = {}
    context['word_db_type'] = word_db_type
    context['word_type'] = word_type
    context['error'] = ''

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['用户名'], password=request.POST['密码'])
        if user is None:
            context['error'] = '用户名或密码错误'
            return render_to_response('home.html', context)
        else:
            context['user'] = user
            login(request, user)
            # context['error'] = ''
            list_data(word_type, context)
            return render_to_response('home.html', context)
    else:
        if request.user.is_authenticated:
            context['user'] = request.user
            list_data(word_type, context)
            return render_to_response('home.html', context)
        else:
            context['error'] = '未登录'
            return render_to_response('home.html', context)

# 退出登录
def user_out(request):
    logout(request)
    return redirect('home')

# 注册
def register(request):
    context = {}
    if request.method == 'POST':
        context['register_form'] = UserCreationForm(request.POST)
        if context['register_form'].is_valid():
            context['register_form'].save()
            user = authenticate(username=context['register_form'].cleaned_data['username'], password=context['register_form'].cleaned_data['password1'])
            context['user'] = user
            login(request, user)
            word_db_type = WordDbType.objects.all()
            word_type = get_object_or_404(WordDbType, pk=1)
            context['word_db_type'] = word_db_type
            context['word_type'] = word_type
            context['error'] = ''
            return render_to_response('home.html', context)
            # return redirect('home', context)
    else:
        context['register_form'] = UserCreationForm()
    print(context['register_form'].errors)
    return render_to_response('register.html', context)

# 选择词库的主页
@login_required(login_url='home')
def band_with_type(request, word_type_pk):
    word_db_type = WordDbType.objects.all()
    word_type = get_object_or_404(WordDbType, pk=word_type_pk)

    context = {}
    context['word_db_type'] = word_db_type
    context['word_type'] = word_type
    # context['already'] = 'yes'
    context['user'] = request.user
    list_data(word_type, context)
    return render_to_response('home.html', context)

# 查看已经学习的单词页面
@login_required(login_url='home')
def view_page(request, word_type_pk):
    word_type = get_object_or_404(WordDbType, pk=word_type_pk)
    word_db_type = WordDbType.objects.all()
    percent_list = {}
    for types in word_db_type:
        word_list = Word.objects.filter(word_db_type=types)
        user_word = UserWord.objects.filter(player=request.user, english__in=word_list)
        percent_list[types] = [types.pk, user_word.count(), word_list.count()]
    # print(percent_list)

    context = {}
    context['word_type'] = word_type
    # context['word_db_type'] = word_db_type
    context['percent_list'] = percent_list
    return render_to_response('view_completed.html', context)

# 查看已经学习的单词内容
@login_required(login_url='home')
def view_content(request, word_type_pk):
    word_type = get_object_or_404(WordDbType, pk=word_type_pk)
    word_list = Word.objects.filter(word_db_type=word_type)
    user_word = UserWord.objects.filter(player=request.user, english__in=word_list).order_by('english')
    
    context = {}
    context['user_word'] = user_word
    return render_to_response('view_content.html', context)
