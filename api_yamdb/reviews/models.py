from django.conf import settings
from django.db import models
from django.db.models import Avg

from .validators import validate_year


class CommonCategoryGenre(models.Model):
    """Базовая модель для категории и жанров"""
    name = models.CharField(
        max_length=254,
        unique=True,
    )
    slug = models.SlugField(
        default='empty',
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.name


class Category(CommonCategoryGenre):
    """Модель для категории"""
    pass


class Genre(CommonCategoryGenre):
    """Модель для жанров"""
    pass


class CommonDatePublished(models.Model):
    """Обстрактная моделя с датой публикации"""
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Review(CommonDatePublished):
    """Модель отзывов"""
    SCORE = ((i, i) for i in range(1, 11))
    text = models.TextField()
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(choices=SCORE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='score_once'
            )
        ]

    def __str__(self) -> str:
        return self.text


class Title(models.Model):
    """Модель для произведений"""
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='genre',
    )
    name = models.CharField(max_length=255)
    year = models.IntegerField(db_index=True, validators=[validate_year])
    description = models.TextField(blank=True)

    @property
    def rating(self) -> int:
        if self._rating is not None:
            return self._rating
        return self.reviews.aggregate(Avg('score'))['rating']

    class Meta:
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.name


class Comment(CommonDatePublished):
    """Модель комментариев"""
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.text
