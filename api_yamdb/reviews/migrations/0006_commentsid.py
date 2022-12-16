# Generated by Django 3.2 on 2022-12-16 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_rewiewstitle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='review',
            new_name='review_id',
        ),
        migrations.AlterField(
            model_name='comments',
            name='review_id',
            field=models.ForeignKey(db_column='review_id', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.reviews'),
        ),
    ]