from django import forms
from django.contrib.auth.models import User
from . import models

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrong':
            raise forms.ValidationError("Wrong password")
        return data

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def save(self):
        return User.objects.create_user(**self.cleaned_data)
    
class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['name', 'text', 'tags']

    def save(self, request):
        question = models.Question()
        question.name = self.cleaned_data["name"]
        question.text = self.cleaned_data["text"]
        question.user = models.Profile.objects.get(user=request.user)
        like = models.Like()
        like.save()
        question.like = like
        question.save()
        question.tags.set(self.cleaned_data["tags"])
        question.save()
        return question
    
class NewAnswerForm(forms.Form):
    Add_answer = forms.CharField(widget=forms.Textarea)

    def save(self, question_id):
        answer = models.Answer()
        answer.text = self.cleaned_data["Add_answer"]
        answer.question = models.Question.objects.get(id=question_id)
        like = models.Like()
        like.save()
        answer.like = like
        answer.save()
        return answer