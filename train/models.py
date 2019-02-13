from django.db import models
from django.contrib.auth.models import User

class WordDbType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

class Word(models.Model):
    word_db_type = models.ForeignKey(WordDbType, on_delete=models.DO_NOTHING)
    first_letter = models.CharField(max_length=1)
    english = models.CharField(max_length=50)
    phonetic_symbol = models.CharField(max_length=50)
    chinese = models.TextField()



