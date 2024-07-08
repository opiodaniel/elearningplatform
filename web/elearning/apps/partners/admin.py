from __future__ import unicode_literals
from django.contrib import admin
from .models import (InstitutionWeb, Course, Program, PersonsPhrase, Category, Event, WhyUS, Services)
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin, TranslatableStackedInline, TranslatableTabularInline

from .models import (Partners, Instructors, Publications)


@admin.register(InstitutionWeb)
class InstitutionWebAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'institution_name', )


@admin.register(Course)
class CourseAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'course_name', 'is_active', )
    list_filter = ('is_active', 'is_popular', )


@admin.register(Program)
class ProgramAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'program_name', 'program_description', 'is_popular', )
    list_filter = ('is_active', 'is_popular', )


@admin.register(Services)
class ServicesAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'service_name', 'service_description',)
    list_filter = ('is_active',)


@admin.register(PersonsPhrase)
class PersonsPhraseAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'persons_name', 'persons_phrase', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'category_name', 'is_active')
    list_filter = ('is_active',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'event_name', 'is_active')
    list_filter = ('is_active',)


@admin.register(WhyUS)
class WhyUSAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'description', 'title', 'icon_name')


class PartnersAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('owner', 'organization_name')


class InstructorsAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('user', )


class PublicationsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'year', 'instructor')


admin.site.register(Partners, PartnersAdmin)
admin.site.register(Instructors, InstructorsAdmin)
admin.site.register(Publications, PublicationsAdmin)

