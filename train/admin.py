from django.contrib import admin
from .models import WordDbType, Word

@admin.register(WordDbType)
class WordDbTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word_db_type', 'first_letter', 'english', 'phonetic_symbol', 'chinese')

