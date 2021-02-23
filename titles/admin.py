from django.contrib import admin

from .models import Category, Genre, Title


# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
