from . import models
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    page_obj = paginator(request, models.Question.objects.GetNewQuestions())
    context = {'tags': models.Tag.objects.GetTopTags(),
               'page_obj': page_obj,
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'index.html', context)

def hot(request):
    page_obj = paginator(request, models.Question.objects.GetTopQuestions())

    context = {'tags': models.Tag.objects.GetTopTags(),
               'page_obj': page_obj,
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'hot.html', context)

def question(request, question_id):
    page_obj = paginator(request, models.Answer.objects.GetTopAnswersOnQuestion(question_id))
    context = {'question': models.Question.objects.GetQuestionById(question_id),
               'tags': models.Tag.objects.GetTopTags(),
               'page_obj': page_obj,
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'question.html', context)


def login(request):
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'login.html', context)


def settings(request):
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'settings.html', context)


def signin(request):
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'signin.html', context)


def ask(request):
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'ask.html', context)


def tags(request, tag_id):
    tag = models.Tag.objects.GetTagById(tag_id)
    page_obj = paginator(request, models.Question.objects.GetTopQuestionsOnTag(tag_id))
    context = {'tag': tag,
               'tags': models.Tag.objects.GetTopTags(),
               'page_obj': page_obj,
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'tags.html', context)


def paginator(request, model):
    contact_list = model
    paginator = Paginator(contact_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj