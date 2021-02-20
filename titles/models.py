from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()

class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Title',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Text',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='reviews',
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
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Publication date',
        auto_now_add=True,
    )
