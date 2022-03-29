import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UUIDField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Абстрактный класс для добавления временных меток моделям-наследникам.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_('Created')
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Updated'))

    class Meta:
        abstract = True


class Genre(TimeStampedModel):
    """
    Жанр кинопроизведения.
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    name = models.CharField(unique=True, max_length=255, verbose_name=_('Title'),)
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'),)

    class Meta:
        db_table = 'content"."genre'
        ordering = ('name',)
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre-detail', kwargs={'pk': self.pk})


class Person(TimeStampedModel):
    """
    Персона (актёр/режисёр/сценарист).
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    full_name = models.CharField(max_length=255, verbose_name=_('Full name'),)
    birth_date = models.DateField(blank=True, null=True, verbose_name=_('Birth date'),)

    class Meta:
        db_table = 'content"."person'
        ordering = ('full_name',)
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        constraints = [
            models.UniqueConstraint(fields=['full_name', 'birth_date'], name='unique_person')
        ]

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('person-detail', kwargs={'pk': self.pk})


class FilmworkTypeChoices(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV Show')


class FilmWork(TimeStampedModel):
    """
    Кинопроизведение (фильм/сериал).
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    title = models.CharField(max_length=255, verbose_name=_('Title'),)
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'),)
    creation_date = models.DateField(blank=True, null=True, verbose_name=_('Creation date'),)
    certificate = models.TextField(blank=True, null=True, verbose_name=_('Certificate'),)
    file_path = models.FileField(
        blank=True, null=True, verbose_name=_('File'), upload_to='film_works/',
    )
    rating = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Rating'),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    type = models.CharField(
        max_length=25,
        verbose_name=_('Type'),
        choices=FilmworkTypeChoices.choices,
        default=FilmworkTypeChoices.MOVIE,
    )
    genres = models.ManyToManyField(
        Genre, blank=True, through='FilmWorkGenre', related_name='film_works',
    )
    persons = models.ManyToManyField(
        Person, blank=True, through='FilmWorkPerson', related_name='film_works',
    )

    class Meta:
        db_table = 'content"."film_work'
        ordering = ('title',)
        verbose_name = _('FilmWork')
        verbose_name_plural = _('FilmWorks')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('filmwork-detail', kwargs={'pk': self.pk})


class FilmWorkGenre(models.Model):
    """
    Связь: Кинопроизведения - Жанры кинопроизведений.
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE,)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'),)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('FilmWorkGenre')
        verbose_name_plural = _('FilmWorksGenres')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'], name='unique_filmwork_genre_link'
            )
        ]

    def __str__(self):
        return f'{self.film_work} - {self.genre}'


class FilmworkpersonRoleChoices(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    DIRECTOR = 'director', _('Director')
    WRITER = 'writer', _('Writer')


class FilmWorkPerson(models.Model):
    """
    Связь: Кинопроизведения - Персоны.
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE,)
    person = models.ForeignKey(Person, on_delete=models.CASCADE,)
    role = models.CharField(
        max_length=25,
        verbose_name=_('Role'),
        choices=FilmworkpersonRoleChoices.choices,
        default=FilmworkpersonRoleChoices.ACTOR,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'),)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('FilmWorkPerson')
        verbose_name_plural = _('FilmWorksPersons')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'], name='unique_filmwork_person_role_link'
            )
        ]

    def __str__(self):
        return f'{self.film_work} - {self.person}'
