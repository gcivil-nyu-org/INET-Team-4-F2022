from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import CommentForm, PostForm
from .models import Post


def post_list(request):
    print(request.user.id)
    queryset = Post.objects.order_by('-created_on')

    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = PostForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(False)
            new_comment.author = request.user
            new_comment.save()
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = PostForm()

    refresh_queryset = Post.objects.order_by('-created_on')

    return render(request, 'index.html', {'post_list': refresh_queryset,  "post": refresh_queryset,
            "new_comment": new_comment,
            "comment_form": comment_form,})


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
