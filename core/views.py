# coding=utf-8

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Article, Part, Appoint, Document, Feedback
from datetime import datetime

MAX_ITEMS = 10


def index(request):
    news = Article.objects.filter(part__name='news').order_by('create_time')[:3] or []
    sliders = Article.objects.filter(part__name='slider').order_by('create_time')[:5] or []
    exhibitions = Article.objects.filter(part__name='exhibition').order_by('create_time')[:4] or []
    guides = Article.objects.filter(part__name='guide').order_by('create_time')[:3] or []
    this_year = datetime.now().year
    return render(request, 'core/home.html', {
        'news': news,
        'exhibitions': exhibitions,
        'sliders': sliders,
        'guides': guides,
        'this_year': this_year
    })


@require_POST
def apply_appoint(request):
    if request.POST.get('name') and request.POST.get('phone') and request.POST.get('time') and request.POST.get('amount'):
        appoint = Appoint(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            note=request.POST.get('note'),
            time=request.POST.get('time'),
            amount=request.POST.get('amount')
        )
        appoint.save()
        return HttpResponse("预约成功!")
    else:
        return HttpResponse("必填栏目不得为空!")


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
    year = int(request.GET.get('year'))
    is_doc = False
    try:
        if part_name == 'doc':
            articles = Document.objects.all()
            part_title = '在线文档'
            is_doc = True
        else:
            if not year:
                articles = Article.objects.filter(part__name=part_name)
            else:
                end_year = datetime(year + 1, 1, 1)
                start_year = datetime(year, 1, 1)
                articles = Article.objects.filter(part__name=part_name, create_time__lt=end_year, create_time__gte=start_year)
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


def send_feedback(request):
    content = request.POST.get('content')
    if len(content) < 10:
        return HttpResponse('意见反馈不能少于10个字！')
    else:
        feedback = Feedback(content=content)
        feedback.save()
        return HttpResponse('您的意见已经成功反馈！')