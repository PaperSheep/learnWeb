# Generated by Django 2.1.5 on 2019-02-22 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('train', '0002_auto_20190223_0704'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWordDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='train.Word')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('word_db_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='train.WordDbType')),
            ],
        ),
        migrations.RemoveField(
            model_name='userword',
            name='player',
        ),
        migrations.RemoveField(
            model_name='userword',
            name='word_db_type',
        ),
        migrations.DeleteModel(
            name='UserWord',
        ),
    ]