from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .validators import not_from_the_future

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        null=False,
        unique=True,
        verbose_name='Ссылочное имя'
    )

    class Meta:
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(
        null=False,
        unique=True,
        verbose_name='Ссылочное имя'
    )

    class Meta:
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Тайтл'
    )
    year = models.IntegerField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name='Дата производства',
        validators=[not_from_the_future]
    )
    rating = models.IntegerField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Рейтинг'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name_plural = 'Тайтлы'
        ordering = ['name', '-year', 'rating']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Text',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        verbose_name='Publication date',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author-title_review_relation'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Review',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Publication date',
        auto_now_add=True,
    )
