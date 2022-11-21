# Define badges
from django.db.models import Count
from post.models import Post

# Return a user's posts
def get_posts(user):
    return Post.objects.filter(author=user)


# Calculate total user likes
def total_likes_received(user):
    user_posts = get_posts(user)
    return user_posts.aggregate(total_likes=Count("likes"))["total_likes"] or 0


# Calculate total user dislikes
def total_dislikes_received(user):
    user_posts = get_posts(user)
    return user_posts.aggregate(total_dislikes=Count("dislikes"))["total_dislikes"] or 0


# Calculate like tier
def user_likes_badges_tier(badges, user_likes):
    if user_likes >= 1:
        badges.append("Likes Tier 1: Somebody likes me...")
    if user_likes >= 5:
        badges.append("Likes Tier 2: GOOD TAKE ALERT")
    if user_likes >= 25:
        badges.append("Likes Tier 3: Mr. Popular!")
    if user_likes >= 100:
        badges.append("Likes Tier 4: LIKEFEST EMCEE")


# Calculate dislike tier
def user_dislikes_badges_tier(badges, user_dislikes):
    if user_dislikes >= 1:
        badges.append("Dislikes Tier 1: Did I hurt your feelings?")
    if user_dislikes >= 5:
        badges.append("Dislikes Tier 2: SPICY TAKE ALERT")
    if user_dislikes >= 25:
        badges.append("Dislikes Tier 3: You need to chill")
    if user_dislikes >= 100:
        badges.append("Dislikes Tier 4: CHILLL DAWG")


# Compare likes to dislikes
def balance_badge(badges, user):
    for post in get_posts(user):
        likes = post.likes.count()
        dislikes = post.dislikes.count()
        if (
            likes == dislikes
            and "Balance Badge: I have brought balance to the force." not in badges
        ):
            badges.append("Balance Badge: I have brought balance to the force.")
        if likes < dislikes and "Controvertial Take Badge: Too honest?" not in badges:
            badges.append("Controvertial Take Badge: Too honest?")
        if likes > dislikes and "Good Take Badge: Right?!" not in badges:
            badges.append("Good Take Badge: Right?!")


# Friends tier
def user_friends_tier(badges, friends):
    if len(friends) >= 1:
        badges.append("Friends Tier 1: Friendly")
    if len(friends) >= 5:
        badges.append("Friends Tier 2: You can't sit with us.")
    if len(friends) >= 25:
        badges.append("Friends Tier 3: I get invited to ALL the parties.")
    if len(friends) >= 100:
        badges.append("Friends Tier 4: Prom Royalty")


# Posts count
def post_tier(badges, user):
    posts = Post.objects.filter(author=user)
    post_count = 0
    for post in posts:
        post_count += 1

    if post_count >= 1:
        badges.append("Posts Tier 1: I'm awake")
    if post_count >= 5:
        badges.append("Posts Tier 2: I have opinions.")
    if post_count >= 25:
        badges.append("Posts Tier 3: Raged and Engaged")
    if post_count >= 100:
        badges.append("Posts Tier 4: KNOW IT ALL")


# Comments count
# def comments_tier():
# How to access comments by user?

#
