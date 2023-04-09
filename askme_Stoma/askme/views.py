from . import models
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    page_obj = paginator(request, models.Question.objects.GetNewQuestions())
    generateUser()
    generateProfile()
    generateQuestion()
    generateAnswer()
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

def generateUser():
    list = []
    for i in range(10000):
        newUser = models.User(username=f'abobaUser{i}', email=f'aboba{i}@crazymail.com', password=f'mypassword{i}')
        list.append(newUser)
    models.User.objects.bulk_create(list)

def generateProfile():
    profiles = [models.Profile(user=models.User.objects.filter(id=i)[0], avatar='gigachad-avatar.jpg') for i in range(1, 10001)]
    models.Profile.objects.bulk_create(profiles)

def generateQuestion():
    count = 1
    j = 0
    for abobaUser in models.Profile.objects.all():
        questions = [models.Question(user=abobaUser, name=f'Awesome Question{i}', text=f'{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...',
                                     like=models.Like.objects.create(rating=i)) for i in range((count - 1) * 10,(count - 1) * 10 + 10)]
        
        for question in questions:
            for i in range(j, j + 3):
                question.save()
                tag = models.Tag.objects.get_or_create(name=f'tag {i}')
                question.tags.add(tag[0])
        count += 1
        if (count % 3 == 0):
            j = count
            

def generateAnswer():
    count = 1
    for abobaQuestion in models.Question.objects.all():
        answers = [models.Answer(question=abobaQuestion, text=f'{i} Ultrices gravida dictum fusce ut placerat orci nulla pellentesque dignissim. Pretium nibh ipsum consequat nisl vel pretium lectus quam. Molestie nunc non blandit massa enim nec. Vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor.',
                                 like=models.Like.objects.create(rating=i)) for i in range((count - 1) * 10,(count - 1) * 10 + 10)]
        count += 1
        models.Answer.objects.bulk_create(answers)