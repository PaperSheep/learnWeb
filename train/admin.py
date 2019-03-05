from django.contrib import admin
from .models import WordDbType, Word, UserWord

@admin.register(WordDbType)
class WordDbTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id' ,'word_db_type', 'first_letter', 'english', 'phonetic_symbol', 'chinese')

@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'english', 'review_time', 'review_count', 'mastery_level')

