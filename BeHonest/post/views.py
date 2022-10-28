from django.shortcuts import get_object_or_404, render
# from django.views import generic

from .forms import CommentForm, PostForm
from .models import Post


def post_list(request):
    queryset = Post.objects.filter(status=1).order_by('-created_on')

    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = PostForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = queryset
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = PostForm()

    return render(request, 'index.html', {'post_list': queryset,  "post": queryset,
            "new_comment": new_comment,
            "comment_form": comment_form,})


def post_detail(request, slug):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
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
