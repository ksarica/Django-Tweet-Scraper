"""CsvToDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from csvfile.views import index
from csvfile.views import tweet_upload,display_tweets


urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls, name="admin"),
    path('upload-csv/', tweet_upload,  name="tweet_upload"),
    path('display-tweets', display_tweets, name="display_tweets")
]
