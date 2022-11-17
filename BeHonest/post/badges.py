# Define badges
from django.db.models import Count
from post.models import Post

def total_likes_received(user):
    user_posts = Post.objects.filter(author=user)
    return user_posts.aggregate(total_likes=Count('likes'))['total_likes'] or 0

def user_likes_badges_tier(user_likes):
    user_like_tiers = []
    if user_likes >= 1:
        user_like_tiers.append("Tier 1")
    
    return user_like_tiers