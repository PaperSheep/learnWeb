from django.urls import path
from . import views


urlpatterns = [
    path('finished/', views.finished, name='finished'),  # 单词学完的跳转页面
    path('level_one/<str:first_letter>/<str:word_type_type_name>', views.word_train, name='word_train'),
    path('level_tow/', views.level_tow, name='level_tow'),
    path('level_three/', views.level_three, name='level_three'),
    path('test/', views.test),  # 测试
]


