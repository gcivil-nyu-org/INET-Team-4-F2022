from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import CommentForm, PostForm, NewsForm
from news.models import News
from post.models import Post
from django.db.models import Count
from .badges import total_likes_received, user_likes_badges_tier

from main.models import FriendRequest, Friend


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

        refresh_queryset = Post.objects.order_by("-created_on")
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


def post_author(request):

    if request.user is not None:
        if request.method == "POST":
            if "link" in request.POST:
                post_form = PostForm()
                new_post = None
                new_post = post_form.save(False)
                auto_populate = request.POST["link"]
                refresh_queryset = Post.objects.annotate(count=Count("likes")).order_by(
                    "-count"
                )
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

        refresh_queryset = Post.objects.annotate(count=Count("likes")).order_by(
            "-count"
        )
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
        print("got firneds")
    except Friend.DoesNotExist:
        print("here")
        friends = []

    # Calculate user badges
    total_likes = total_likes_received(authenticated_user)
    badges = user_likes_badges_tier(total_likes)
    print(alreadySent)

    context = {
        "user": user,
        "posts": logged_in_user_posts,
        "friend_requests": friend_requests,
        "authenticated_user": authenticated_user,
        "friends": friends,
        "isFriend": isFriend,
        "alreadySent": alreadySent,
        "badges": badges,
    }

    return render(request, "profile.html", context)
