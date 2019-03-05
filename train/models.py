from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone

class WordDbType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

class Word(models.Model):
    word_db_type = models.ForeignKey(WordDbType, on_delete=models.DO_NOTHING)
    first_letter = models.CharField(max_length=50)
    english = models.CharField(max_length=50)
    phonetic_symbol = models.CharField(max_length=50)
    chinese = models.TextField()

    def __str__(self):
        return self.english

class UserWord(models.Model):
    player = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # word_db_type = models.ForeignKey(WordDbType, on_delete=models.DO_NOTHING)
    english = models.ForeignKey(Word, on_delete=models.DO_NOTHING)
    review_time = models.DateTimeField('复习时间', default = timezone.now)
    review_count = models.IntegerField('复习次数', default = 0)
    mastery_level = models.FloatField('掌握程度', default = 50)
