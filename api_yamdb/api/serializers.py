from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Reviews, Comments


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'category', 'genre', 'year', 'description')
        model = Title

    validators = (
        UniqueTogetherValidator(
            queryset=Title.objects.all(),
            fields=('name', 'category'),
            message='Произведение уже привязано к категории!'
        ),
    )

    def validate(self, data):
        if self.data['year'] > datetime.now().year:
            raise serializers.ValidationError('Такой год еще не наступил!')
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'text', 'score')
        model = Reviews


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'review', 'text')
        model = Comments

# По тз 1 юзер может добавить только 1 отзыв,
# пока не нашёл как это реализовать, если у вас есть идеи, с радостью выслушаю
