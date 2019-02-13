from django.urls import path
from . import views


urlpatterns = [
    path('level_one/<str:first_letter>/', views.word_train, name='word_train'),
    path('level_tow/', views.level_tow, name='level_tow'),
    path('level_three/', views.level_three, name='level_three'),
]


