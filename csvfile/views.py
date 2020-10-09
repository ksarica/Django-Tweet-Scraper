import csv, io
from django.shortcuts import render
from django.contrib import messages
from .models import Tweet


# Create your views here.

def index(request):
    template = 'index.html'
    return render(request, template)


def display_tweets(request):
    template = 'display_tweets.html'
    data = Tweet.objects.all()
    all_tweets = {'tweet': data}
    return render(request, template, all_tweets)


def tweet_upload(request):
    # declaring template
    template = 'tweet_upload.html'
    data = Tweet.objects.all()
    prompt = {
        'order': 'Order of the CSV should be author, date, text, comment, retweet, like',
        'profiles': data
    }

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    # check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    file_data = csv_file.read().decode("utf-8")
    rows = file_data.split('\n')

    # Loop over the lines and save them in db. 
    for row in rows:
        if row == rows[0]:
            continue
        if not row.strip():
            continue
        columns = row.split(",")
        Tweet.objects.update_or_create(author=columns[0], date=columns[1], text=columns[2], comment=columns[3],
                                       retweet=columns[4], like=columns[5])
    context = {}
    return render(request, template, context)
