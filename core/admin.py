# coding=utf-8

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Article, Part, Appoint


class PartAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']


class ArticleAdmin(SummernoteModelAdmin):
    list_display = ['title', 'desc', 'part', 'create_time']


class AppointAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'time', 'finished']

admin.site.register(Appoint, AppointAdmin)

admin.site.register(Article, ArticleAdmin)

admin.site.register(Part, PartAdmin)