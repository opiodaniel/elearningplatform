from django.contrib import admin
from .models import News
from cms.admin.placeholderadmin import PlaceholderAdminMixin


@admin.register(News)
class NewsAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'topic_name')

# Register your models here.
