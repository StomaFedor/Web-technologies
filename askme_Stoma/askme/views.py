from . import models
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
def index(request):

    page_obj = paginator(request, models.QUESTIONS)

    context = {'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'page_obj': page_obj}
    return render(request, 'index.html', context)


def question(request, question_id):
    if len(models.QUESTIONS) <= question_id:
        question_id = len(models.QUESTIONS) - 1
    
    page_obj = paginator(request, models.ANSWERS)

    context = {'answers': models.ANSWERS,
               'question': models.QUESTIONS[question_id],
               'tags': models.TAGS,
               'page_obj': page_obj}
    return render(request, 'question.html', context)


def login(request):
    context = {'tags': models.TAGS}
    return render(request, 'login.html', context)


def settings(request):
    context = {'tags': models.TAGS}
    return render(request, 'settings.html', context)


def signin(request):
    context = {'tags': models.TAGS}
    return render(request, 'signin.html', context)


def ask(request):
    context = {'tags': models.TAGS}
    return render(request, 'ask.html', context)


def tags(request, tag_id):
    
    if len(models.TAGS) <= tag_id:
        tag_id = len(models.TAGS) - 1
    
    page_obj = paginator(request, models.QUESTIONS)

    context = {'tag': models.TAGS[tag_id],
               'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'page_obj': page_obj}
    return render(request, 'tags.html', context)


def paginator(request, model):
    contact_list = model
    paginator = Paginator(contact_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj