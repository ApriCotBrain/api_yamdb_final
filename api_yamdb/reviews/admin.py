from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from reviews.models import Category, Genre, Title


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = (
        'name',
        'slug',
    )


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = (
        'name',
        'slug',
    )
