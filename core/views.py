# coding=utf-8

from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import serialize
from .models import Article, Part, Appoint

MAX_ITEMS = 10


def index(request):
    news = Article.objects.filter(part__name='news').order_by('create_time')[:3] or []
    sliders = Article.objects.filter(part__name='slider').order_by('create_time')[:5] or []
    exhibitions = Article.objects.filter(part__name='exhibition').order_by('create_time')[:4] or []

    return render(request, 'core/home.html', {
        'news': news,
        'exhibitions': exhibitions,
        'sliders': sliders
    })


def load_more(request, page=1):
    page = int(page)
    exhibitions_part = Part.objects.get(name='exhibition')
    exhibitions_total = exhibitions_part.article_set.order_by('create_time')[page * 4: (page + 1) * 4] or []
    exhibitions_json = serialize("json", exhibitions_total)
    return HttpResponse(exhibitions_json, content_type="application/json")


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


def article(request, article_id):
    try:
        articles = Article.objects.get(id=article_id)
    except ObjectDoesNotExist:
        articles = None
    return render(request, 'core/article.html', {
        'article': articles
    })


def part(request, part_name):
    page = request.GET.get('page') or 1
    articles = Article.objects.filter(part__name=part_name)
    paginator = Paginator(articles, MAX_ITEMS)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return render(request, 'core/part.html', {
        articles: result
    })
