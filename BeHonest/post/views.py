from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CommentForm, PostForm, NewsForm
from news.models import News
from post.models import Post
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .badges import total_likes_received
from .badges import total_dislikes_received
from .badges import user_likes_badges_tier
from .badges import user_dislikes_badges_tier
from .badges import user_friends_tier
from .badges import post_tier
from .badges import balance_badge
from random import shuffle
from main.models import FriendRequest, Friend
from .user_statistics import most_liked_post, most_disliked_post


@login_required(login_url="/")  # redirect when user is not logged in
def search_results(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        posts = Post.objects.filter(title__contains=searched)
        return render(
            request, "search_results.html", {"searched": searched, "posts": posts}
        )
    else:
        return render(request, "search_results.html", {})


def prof_results(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        profs = User.objects.filter(username__contains=searched)
        return render(
            request, "prof_results.html", {"searched": searched, "profs": profs}
        )
    else:
        return render(request, "prof_results.html", {})


def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    elif post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        post.likes.add(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse("post:post_detail", args=[str(pk)]))


def dislike_post(request, pk):

    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        post.dislikes.add(request.user)
    elif post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return HttpResponseRedirect(reverse("post:post_detail", args=[str(pk)]))


@login_required(login_url="/")  # redirect when user is not logged in
def delete_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    # security check so only current user can delete posts
    if request.user == post.author:
        post.delete()
        return HttpResponseRedirect(reverse("post:base"))


@login_required(login_url="/")  # redirect when user is not logged in
def delete_user(request, pk):
    print(request.user)
    u = get_object_or_404(User, username=request.POST.get("username"))
    if request.user.username == u.username:
        u.delete()
        messages.success(request, "The user is deleted")
        return HttpResponseRedirect(reverse("main:homepage"))
    # try:
    #     u = get_object_or_404(User, username=request.POST.get("username"))
    #     u.delete()
    #     messages.success(request, "The user is deleted")
    #     HttpResponseRedirect(reverse("main:homepage"))
    # except User.DoesNotExist:
    #     messages.error(request, "User does not exist")
    #     redirect_str = "/home/profile/" +str(request.user)
    #     return redirect(redirect_str)
    # except Exception as e:
    #     messages.error(request, {'err':e.message})
    #     redirect_str = "/home/profile/" +str(request.user)
    #     return redirect(redirect_str)


@login_required(login_url="/")  # redirect when user is not logged in
def post_list(request):
    if request.user is not None:
        if request.method == "POST":
            if "link" in request.POST:
                post_form = PostForm()
                new_post = None
                new_post = post_form.save(False)
                auto_populate = request.POST["link"]
                refresh_queryset = Post.objects.order_by("-created_on")
                return render(
                    request,
                    "index.html",
                    {
                        "post_list": refresh_queryset,
                        "post": refresh_queryset,
                        "new_comment": new_post,
                        "comment_form": post_form,
                        "auto_populate": auto_populate,
                    },
                )

        new_post = None
        # Comment posted
        if request.method == "POST":
            post_form = PostForm(data=request.POST)
            if post_form.is_valid():
                # Create Comment object but don't save to database yet
                new_post = post_form.save(False)
                new_post.author = request.user
                # Save the comment to the database
                new_post.save()
        else:
            post_form = PostForm()
        user = get_object_or_404(User, username=str(request.user))

        try:

            friends_list = Friend.objects.filter(primary=user)

        except Friend.DoesNotExist:

            friends_list = []

        usernames = []
        for i in range(0, len(friends_list)):
            usernames.append(friends_list[i].secondary)

        refresh_queryset = Post.objects.filter(author__in=usernames).order_by(
            "-created_on"
        ) | Post.objects.filter(author=user).order_by("-created_on")
        return render(
            request,
            "index.html",
            {
                "post_list": refresh_queryset,
                "post": refresh_queryset,
                "new_comment": new_post,
                "comment_form": post_form,
            },
        )


@login_required(login_url="/")  # redirect when user is not logged in
def post_author(request):

    if request.user is not None:
        if request.method == "POST":
            if "link" in request.POST:
                post_form = PostForm()
                new_post = None
                new_post = post_form.save(False)
                auto_populate = request.POST["link"]
                user = get_object_or_404(User, username=str(request.user))

                try:

                    friends_list = Friend.objects.filter(primary=user)

                except Friend.DoesNotExist:

                    friends_list = []

                usernames = []
                for i in range(0, len(friends_list)):
                    usernames.append(friends_list[i].secondary)

                refresh_queryset = Post.objects.filter(author__in=usernames).annotate(
                    count=Count("likes")
                ).order_by("-count") | Post.objects.filter(author=user).annotate(
                    count=Count("likes")
                ).order_by(
                    "-count"
                )
                # refresh_queryset = Post.objects.annotate(count=Count("likes")).order_by(
                #     "-count"
                # )
                return render(
                    request,
                    "sort.html",
                    {
                        "post_author": refresh_queryset,
                        "post": refresh_queryset,
                        "new_comment": new_post,
                        "comment_form": post_form,
                        "auto_populate": auto_populate,
                    },
                )

        new_post = None
        # Comment posted
        if request.method == "POST":
            post_form = PostForm(data=request.POST)
            if post_form.is_valid():
                # Create Comment object but don't save to database yet
                new_post = post_form.save(False)
                new_post.author = request.user
                # Save the comment to the database
                new_post.save()
        else:
            post_form = PostForm()

        user = get_object_or_404(User, username=str(request.user))

        try:

            friends_list = Friend.objects.filter(primary=user)

        except Friend.DoesNotExist:

            friends_list = []

        usernames = []
        for i in range(0, len(friends_list)):
            usernames.append(friends_list[i].secondary)

        refresh_queryset = Post.objects.filter(author__in=usernames).annotate(
            count=Count("likes")
        ).order_by("-count") | Post.objects.filter(author=user).annotate(
            count=Count("likes")
        ).order_by(
            "-count"
        )

        # refresh_queryset = Post.objects.annotate(count=Count("likes")).order_by(
        #    "-count"
        # )
        return render(
            request,
            "sort.html",
            {
                "post_author": refresh_queryset,
                "post": refresh_queryset,
                "new_comment": new_post,
                "comment_form": post_form,
            },
        )


@login_required(login_url="/")  # redirect when user is not logged in
def post_detail(request, id):
    """

    :param request:
    :type request:
    :param id:
    :type id:
    :return:
    :rtype:
    """
    template_name = "post_detail.html"
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    post.liked = False
    post.disliked = False
    if post.likes.filter(id=request.user.id).exists():
        post.liked = True
    if post.dislikes.filter(id=request.user.id).exists():
        post.disliked = True
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

@login_required(login_url="/")  # redirect when user is not logged in
def news_detail(request, id):
    """

    :param request:
    :type request:
    :return:
    :rtype:
    """
    template_name = "news_detail.html"
    post = get_object_or_404(News, id=id)
    comments = post.newscomment.filter(active=True).order_by("-created_on")
    new_comment = None

    # Comment posted
    if request.method == "POST":
        comment_form = NewsForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = NewsForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

@login_required(login_url="/")  # redirect when user is not logged in
def profile(request, pk):
    user = User.objects.get(username=pk)
    authenticated_user = request.user

    logged_in_user_posts = Post.objects.filter(author=user)
    try:
        friend_requests = FriendRequest.objects.filter(receiver=user, status="pending")
    except FriendRequest.DoesNotExist:
        friend_requests = []

    try:
        friends = Friend.objects.get(primary=user, secondary=authenticated_user)
        isFriend = True
    except Friend.DoesNotExist:
        isFriend = False

    friend_requests = FriendRequest.objects.filter(
        receiver=authenticated_user, status="pending"
    )
    already_sent = FriendRequest.objects.filter(
        sender=authenticated_user, receiver=user, status="pending"
    )
    print(friend_requests)
    if already_sent:
        alreadySent = True

    else:
        alreadySent = False

    try:

        friends = Friend.objects.filter(primary=user)
        # print("got firneds")
    except Friend.DoesNotExist:
        print("here")
        friends = []

    print(alreadySent)

    # Calculate user badges
    badges = []

    # 1. Likes related badges
    total_likes = total_likes_received(user)
    user_likes_badges_tier(badges, total_likes)

    # 2. Dislike related badges
    total_dislikes = total_dislikes_received(user)
    user_dislikes_badges_tier(badges, total_dislikes)

    # 3. Balance badge
    balance_badge(badges, user)

    # 4. Friends badge
    user_friends_tier(badges, friends)

    # 5. Posts badge
    post_tier(badges, user)

    # Caclulate Remaining Badges
    remaining_badges = 19 - len(badges)

    # Randomize display order of badges
    shuffle(badges)

    # Identify best and worst posts
    if authenticated_user == user:
        top_post = most_liked_post(user)
        bottom_post = most_disliked_post(user)
    else:
        top_post = ""
        bottom_post = ""

    context = {
        "user": user,
        "posts": logged_in_user_posts,
        "friend_requests": friend_requests,
        "authenticated_user": authenticated_user,
        "friends": friends,
        "isFriend": isFriend,
        "alreadySent": alreadySent,
        "badges": badges,
        "likes": total_likes,
        "dislikes": total_dislikes,
        "badges_remaining": remaining_badges,
        "top_post": top_post,
        "bottom_post": bottom_post,
    }

    return render(request, "profile.html", context)
