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
        badges.append([1, "Likes", "Somebody likes me..."])
    if user_likes >= 5:
        badges.append([2, "Likes", "GOOD TAKE ALERT"])
    if user_likes >= 25:
        badges.append([3, "Likes", "Mr. Popular!"])
    if user_likes >= 100:
        badges.append([4, "Likes", "LIKEFEST EMCEE"])


# Calculate dislike tier
def user_dislikes_badges_tier(badges, user_dislikes):
    if user_dislikes >= 1:
        badges.append([1, "Dislikes", "Did I hurt your feelings?"])
    if user_dislikes >= 5:
        badges.append([2, "Dislikes", "SPICY TAKE ALERT"])
    if user_dislikes >= 25:
        badges.append([3, "Dislikes", "You need to chill"])
    if user_dislikes >= 100:
        badges.append([4, "Dislikes", "CHILLL DAWG"])


# Compare likes to dislikes
def balance_badge(badges, user):
    for post in get_posts(user):
        likes = post.likes.count()
        dislikes = post.dislikes.count()
        if (
            likes == dislikes
            and [0, "Balance Badge", "I have brought balance to the force."] not in badges
        ):
            badges.append([0, "Balance Badge", "I have brought balance to the force."])
        if likes < dislikes and [0, "Controvertial Take Badge", "Too honest?"] not in badges:
            badges.append([0, "Controvertial Take Badge", "Too honest?"])
        if likes > dislikes and [0, "Good Take Badge", "Right?!"] not in badges:
            badges.append([0, "Good Take Badge", "Right?!"])


# Friends tier
def user_friends_tier(badges, friends):
    if len(friends) >= 1:
        badges.append([1, "Friends", "Friendly"])
    if len(friends) >= 5:
        badges.append([2, "Friends", "You can't sit with us."])
    if len(friends) >= 25:
        badges.append([3, "Friends", "I get invited to ALL the parties."])
    if len(friends) >= 100:
        badges.append([4, "Friends", "Prom Royalty"])


# Posts count
def post_tier(badges, user):
    posts = Post.objects.filter(author=user)
    post_count = 0
    for post in posts:
        post_count += 1

    if post_count >= 1:
        badges.append([1, "Posts", "I'm awake."])
    if post_count >= 5:
        badges.append([2, "Posts", "I have opinions."])
    if post_count >= 25:
        badges.append([3, "Posts", "Raged and Engaged."])
    if post_count >= 100:
        badges.append([4, "Posts", "KNOW IT ALL."])