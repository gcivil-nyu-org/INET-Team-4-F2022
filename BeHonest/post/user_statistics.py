from post.models import Post


# Return most liked post
def most_liked_post(user):
    posts = Post.objects.filter(author=user)

    max_likes = 0
    most_liked_post = posts[0]

    for post in posts:
        if post.total_likes() > max_likes:
            max_likes = post.total_likes()
            most_liked_post = post
    
    return most_liked_post


# Return most disliked posts
def most_disliked_post(user):
    posts = Post.objects.filter(author=user)

    max_dislikes = 0
    most_disliked_post = posts[0]

    for post in posts:
        if post.total_dislikes() > max_dislikes:
            max_dislikes = post.total_dislikes()
            most_disliked_post = post
    
    return most_disliked_post