from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, FilmworkpersonRoleChoices


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ('get',)

    def get_queryset(self):
        return FilmWork.objects.all()

    def render_to_response(self, context, **kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, **kwargs):
        queryset = list(
            self.get_queryset()
            .values('id', 'title', 'description', 'creation_date', 'rating', 'type')
            .annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(filmworkperson__role__iexact=FilmworkpersonRoleChoices.ACTOR),
                    distinct=True,
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(filmworkperson__role__iexact=FilmworkpersonRoleChoices.DIRECTOR),
                    distinct=True,
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(filmworkperson__role__iexact=FilmworkpersonRoleChoices.WRITER),
                    distinct=True,
                ),
            )
        )

        paginator, page, results, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': results,
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        result = (
            self.get_queryset()
            .filter(pk=self.object.pk)
            .values('id', 'title', 'description', 'creation_date', 'rating', 'type')
            .annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(filmworkperson__role__iexact=FilmworkpersonRoleChoices.ACTOR),
                    distinct=True,
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(filmworkperson__role__iexact=FilmworkpersonRoleChoices.DIRECTOR),
                    distinct=True,
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(filmworkperson__role__iexact=FilmworkpersonRoleChoices.WRITER),
                    distinct=True,
                ),
            )
            .first()
        )
        print(type(result))
        return result
