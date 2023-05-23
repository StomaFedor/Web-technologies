from askme.forms import RegistrationForm
from . import models
from askme.forms import LoginForm , NewQuestionForm, NewAnswerForm

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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
    if (request.method == 'GET'):
        answer_form = NewAnswerForm()
    elif (request.method == 'POST'):
        answer_form = NewAnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(question_id)
            if answer:
                return redirect(reverse('question', kwargs={'question_id':question_id}))
            answer_form.add_error(None, "Answer save error!")
    page_obj = paginator(request, models.Answer.objects.GetTopAnswersOnQuestion(question_id))
    context = {'question': models.Question.objects.GetQuestionById(question_id),
               'tags': models.Tag.objects.GetTopTags(),
               'page_obj': page_obj,
               'profiles': models.Profile.objects.GetTopUsers(),
               'form': answer_form}
    return render(request, 'question.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


def login(request):
    if (request.method == 'GET'):
        login_form = LoginForm()
    elif (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                if request.GET.get('continue'):
                    return redirect(request.GET.get('continue'))
                else:
                    return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers(),
               'form': login_form}
    return render(request, 'login.html', context)


@login_required(login_url='/login', redirect_field_name='continue')
def settings(request):
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers()}
    return render(request, 'settings.html', context)


def signin(request):
    if (request.method == 'GET'):
        user_form = RegistrationForm()
    elif (request.method == 'POST'):
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            user_form.add_error(None, "User save error!")
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers(),
               'form': user_form}
    return render(request, 'signin.html', context)


@login_required(login_url='/login', redirect_field_name='continue')
def ask(request):
    if (request.method == 'GET'):
        question_form = NewQuestionForm()
    elif (request.method == 'POST'):
        question_form = NewQuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(request)
            if question:
                return redirect(reverse('question', kwargs={'question_id':question.id}))
            question_form.add_error(None, "Question save error!")
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers(),
               'form': question_form}
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