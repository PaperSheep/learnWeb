"""LearnEnglish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 主页
    path('logout/', views.user_out, name='user_out'),  # 注销
    path('register', views.register, name='register'),  # 注册
    path('admin/', admin.site.urls),  # 后台
    path('train/', include('train.urls')),  # 训练页面 
    path('band/<int:word_type_pk>', views.band_with_type, name='band_with_type'),  # 选择词库
    path('view/<int:word_type_pk>', views.view_page, name='view_page'),  # 查看已学完单词的页面
    path('content/<int:word_type_pk>', views.view_content, name='view_content'),  # 查看已学完单词的内容
]
