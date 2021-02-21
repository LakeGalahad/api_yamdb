from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Genre, Review, Comment, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['name'],
            )
        ]


class TitlesCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
        model = Title


class TitlesListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message=('You can review a title only once!'
                         'Consider partial update of your review.')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
