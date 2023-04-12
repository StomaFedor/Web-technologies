from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileManager(models.Manager):
    def GetTopUsers(self):
        Users = self.annotate(qCount=models.Count('question')) 
        return Users.order_by('-qCount')[:3]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default=0)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):
    def GetTopQuestions(self):
        return self.order_by('-like__rating')
    
    def GetNewQuestions(self):
        return self.order_by('-data')
    
    def GetQuestionById(self, question_id):
        if self.filter(id=question_id).exists():
            return self.get(id=question_id)
        return self.last()
    
    def GetTopQuestionsOnTag(self, tag_id):
        return self.filter(tags__id=tag_id).order_by('-like__rating') 

class Question(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
    like = models.OneToOneField('Like', on_delete=models.PROTECT)
    data = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')

    objects = QuestionManager()

    def __str__(self):
        return f'id={self.id}; user_name={self.user}'


class AnswerManager(models.Manager):
    def GetTopAnswersOnQuestion(self, question_id):
        return self.filter(question__id=question_id).order_by('-correct')

class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    correct = models.BooleanField(default=False)
    like = models.OneToOneField('Like', on_delete=models.PROTECT)

    objects = AnswerManager()

    def __str__(self):
        return f'id={self.id}; question_id={self.question.id}'


class TagManager(models.Manager):
    def GetTagById(self, tag_id):
        if self.filter(id=tag_id).exists():
            return self.get(id=tag_id)
        return self.last()
    
    def GetTopTags(self):
        tags = self.annotate(qCount=models.Count('question')) 
        return tags.order_by('-qCount')[:5]
    
class Tag(models.Model):
    name = models.CharField(max_length=255)

    objects = TagManager()

    def __str__(self):
        return self.name


class Like(models.Model):
    rating = models.IntegerField(default=0)
    likedProfile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'id={self.id}; likes={self.rating}'