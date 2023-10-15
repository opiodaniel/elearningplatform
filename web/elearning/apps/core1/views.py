from django.shortcuts import render
from.models import News


def home(request):
    title = 'Core1 App'
    news = News.objects.all()
    # print(news[0].topic_name)
    # news_ = news[0].description
    return render(request, 'core1/main.html', {'title': title, 'news': news})

