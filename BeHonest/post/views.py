from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import CommentForm, PostForm
from .models import Post


# needed to add this function here to go back to blank main page
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:homepage")


def post_list(request):

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


def post_detail(request, id):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
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
