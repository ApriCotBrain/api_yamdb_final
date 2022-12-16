# Generated by Django 3.2 on 2022-12-16 13:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0004_rewiewstitleiddelete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='title',
            new_name='title_id',
        ),
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together={('title_id', 'author')},
        ),
    ]