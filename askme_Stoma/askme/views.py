from django.http import HttpResponse, JsonResponse
from . import models
from askme.forms import LoginForm, RegistrationForm, NewQuestionForm, NewAnswerForm, SettingsForm

from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST


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
@require_http_methods(['GET', 'POST'])
def settings(request):
    if (request.method == 'GET'):
        data = model_to_dict(request.user)
        settings_form = SettingsForm(initial=data)
    elif (request.method == 'POST'):
        settings_form = SettingsForm(request.POST, files=request.FILES, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
    context = {'tags': models.Tag.objects.GetTopTags(),
               'profiles': models.Profile.objects.GetTopUsers(),
               'form': settings_form}
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

@login_required(login_url='/login', redirect_field_name='continue')
@require_POST
def question_vote_up(request):
    question_id = request.POST['question_id']
    question = models.Question.objects.get(id=question_id)
    if models.LikeQuestion.objects.filter(question=question, profile=request.user.profile).exists():
        like = models.LikeQuestion.objects.get(question=question, profile=request.user.profile)
        if like.rate == False:
            like.delete()
            question.rating += 1
            question.save()
        return JsonResponse({
            'new_rating': question.rating
        })
    like = models.LikeQuestion.objects.create(question=question, profile=request.user.profile, rate=True)
    like.save()
    question.rating += 1
    question.save()
    return JsonResponse({
        'new_rating': question.rating
    })


@login_required(login_url='/login', redirect_field_name='continue')
@require_POST
def question_vote_down(request):
    question_id = request.POST['question_id']
    question = models.Question.objects.get(id=question_id)
    if models.LikeQuestion.objects.filter(question=question, profile=request.user.profile).exists():
        like = models.LikeQuestion.objects.get(question=question, profile=request.user.profile)
        if like.rate == True:
            like.delete()
            question.rating -= 1
            question.save()
        return JsonResponse({
            'new_rating': question.rating
        })
    like = models.LikeQuestion.objects.create(question=question, profile=request.user.profile, rate=False)
    like.save()
    question.rating -= 1
    question.save()
    return JsonResponse({
        'new_rating': question.rating
    })


@login_required(login_url='/login', redirect_field_name='continue')
@require_POST
def answer_vote_down(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    if models.LikeAnswer.objects.filter(answer=answer, profile=request.user.profile).exists():
        like = models.LikeAnswer.objects.get(answer=answer, profile=request.user.profile)
        if like.rate == True:
            like.delete()
            answer.rating -= 1
            answer.save()
        return JsonResponse({
            'new_rating': answer.rating
        })
    like = models.LikeAnswer.objects.create(answer=answer, profile=request.user.profile, rate=False)
    like.save()
    answer.rating -= 1
    answer.save()
    return JsonResponse({
        'new_rating': answer.rating
    })


@login_required(login_url='/login', redirect_field_name='continue')
@require_POST
def answer_vote_up(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    if models.LikeAnswer.objects.filter(answer=answer, profile=request.user.profile).exists():
        like = models.LikeAnswer.objects.get(answer=answer, profile=request.user.profile)
        if like.rate == False:
            like.delete()
            answer.rating += 1
            answer.save()
        return JsonResponse({
            'new_rating': answer.rating
        })
    like = models.LikeAnswer.objects.create(answer=answer, profile=request.user.profile, rate=True)
    like.save()
    answer.rating += 1
    answer.save()
    return JsonResponse({
        'new_rating': answer.rating
    })


def paginator(request, model):
    contact_list = model
    paginator = Paginator(contact_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

@login_required(login_url='/login', redirect_field_name='continue')
@require_POST
def check_field(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    if answer.correct:
        answer.correct = False
    else:
        answer.correct = True
    answer.save()
    return JsonResponse({
        'new_correct': answer.correct
    })