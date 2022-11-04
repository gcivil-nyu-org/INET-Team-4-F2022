from django.shortcuts import render
from newsapi import NewsApiClient
from .models import News


# Create your views here.


def index(request):
    api = NewsApiClient(api_key="084b04d11f594e6a90cb0e4f8b0fab81")
    all_news = {}
    crypto_news = api.get_everything(q="NYC weather")
    a = crypto_news["articles"]
    title = []
    img = []
    url = []
    for i in range(len(a)):
        f = a[i]
        desc = f["description"]
        if News.objects.filter(desc = desc).exists():
            continue
        else:
            news_data = News(
                title=f["title"],
                desc=f["description"],
                img=f["urlToImage"],
                url=f["url"]
            )
            title.append(f["title"])

            img.append(f["urlToImage"])
            url.append(f["url"])
            news_data.save()

    new_post = None
    # Comment posted
    refresh_queryset = News.objects.order_by("desc")
    return render(
        request,
        "new.html",
        {
            "post_list": refresh_queryset,
            "post": refresh_queryset,
            "new_comment": new_post,
           },
    )
    #
    # mylist = zip(title, desc, img, url)
    #
    # context = {"mylist": mylist}
    #
    # return render(request, "new.html", context)
