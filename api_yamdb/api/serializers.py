from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

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
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if (title.reviews.filter(author=author).exists()
           and self.context.get('request').method != 'PATCH'):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Недопустимое значение!')
        return value


class CommentSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review',)

