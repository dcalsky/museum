# coding=utf-8

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Article, Part, Appoint, Document

MAX_ITEMS = 10


def index(request):
    news = Article.objects.filter(part__name='news').order_by('create_time')[:3] or []
    sliders = Article.objects.filter(part__name='slider').order_by('create_time')[:5] or []
    exhibitions = Article.objects.filter(part__name='exhibition').order_by('create_time')[:4] or []
    guides = Article.objects.filter(part__name='guide').order_by('create_time')[:3] or []
    return render(request, 'core/home.html', {
        'news': news,
        'exhibitions': exhibitions,
        'sliders': sliders,
        'guides': guides
    })


@require_POST
def apply_appoint(request):
    appoint = Appoint(
        name=request.POST.get('name'),
        phone=request.POST.get('phone'),
        note=request.POST.get('note'),
        time=request.POST.get('time'),
        amount=request.POST.get('amount')
    )
    appoint.save()
    return HttpResponse("预约成功!")


def article(request, part_name, article_id):
    try:
        articles = Article.objects.get(id=article_id, part__name=part_name)
    except ObjectDoesNotExist:
        articles = None
    return render(request, 'core/article.html', {
        'article': articles
    })


def part(request, part_name):
    page = request.GET.get('page') or 1
    is_doc = False
    try:
        if part_name == 'doc':
            articles = Document.objects.all()
            part_title = '在线文档'
            is_doc = True
        else:
            articles = Article.objects.filter(part__name=part_name)
            part_title = Part.objects.get(name=part_name).title
        paginator = Paginator(articles, MAX_ITEMS)
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    except ObjectDoesNotExist:
        return redirect('core:index')
    return render(request, 'core/part.html', {
        'is_doc': is_doc,
        'part_name': part_name,
        'part_title': part_title,
        'articles': result,
        'max_page': paginator.num_pages,
        'views': paginator.count * 1089 + 5
    })
