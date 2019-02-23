from django.shortcuts import render_to_response, get_object_or_404, redirect
from train.models import WordDbType, Word
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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
            return render_to_response('home.html', context)
    else:
        if request.user.is_authenticated:
            context['user'] = request.user
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
    return render_to_response('home.html', context)
