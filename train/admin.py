from django.contrib import admin
from .models import WordDbType, Word, UserDbWord

@admin.register(WordDbType)
class WordDbTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id' ,'word_db_type', 'first_letter', 'english', 'phonetic_symbol', 'chinese')

@admin.register(UserDbWord)
class UserDbWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'english')

