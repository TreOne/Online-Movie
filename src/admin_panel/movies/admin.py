from django.contrib import admin

from movies.models import FilmWork, FilmWorkGenre, FilmWorkPerson, Genre, Person


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date')
    search_fields = ('full_name',)


class FilmWorkGenreInline(admin.TabularInline):
    model = FilmWorkGenre
    extra = 1


class FilmWorkPersonInline(admin.TabularInline):
    model = FilmWorkPerson
    raw_id_fields = ('person',)
    extra = 1


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'rating', 'type')
    list_filter = ('type', 'genres')
    search_fields = ('title', 'description')
    date_hierarchy = 'creation_date'
    inlines = (
        FilmWorkGenreInline,
        FilmWorkPersonInline,
    )
