from django.shortcuts import render
from newsapi import NewsApiClient

# Create your views here.


def index(request):
    api = NewsApiClient(api_key="084b04d11f594e6a90cb0e4f8b0fab81")

    crypto_news = api.get_everything(q="NYC weather")
    a = crypto_news["articles"]
    desc = []
    title = []
    img = []
    url = []
    for i in range(len(a)):
        f = a[i]
        title.append(f["title"])
        desc.append(f["description"])
        img.append(f["urlToImage"])
        url.append(f["url"])
    mylist = zip(title, desc, img, url)

    context = {"mylist": mylist}

    return render(request, "new.html", context)
