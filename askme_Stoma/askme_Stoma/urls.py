"""
URL configuration for askme_Stoma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from askme import views
from . import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('hot/', views.hot, name="hot"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('admin/', admin.site.urls),
    path('login', views.login, name="login"),
    path('settings', views.settings, name="settings"),
    path('signin', views.signin, name="signin"),
    path('ask', views.ask, name="ask"),
    path('logout', views.logout, name="logout"),
    path('tags/<int:tag_id>/', views.tags, name="tags"),
    path('question_vote_up/', views.question_vote_up, name='question_vote_up'),
    path('question_vote_down/', views.question_vote_down, name='question_vote_down'),
    path('answer_vote_down/', views.answer_vote_down, name='answer_vote_down'),
    path('answer_vote_up/', views.answer_vote_up, name='answer_vote_up'),
    path('check_field/', views.check_field, name='check_field'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
