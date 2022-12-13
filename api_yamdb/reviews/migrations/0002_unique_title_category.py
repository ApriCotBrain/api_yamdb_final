# Generated by Django 3.2 on 2022-12-13 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_title_category_genre'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='title',
            constraint=models.UniqueConstraint(fields=('name', 'category'), name='unique_title_category'),
        ),
    ]
