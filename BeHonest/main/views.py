from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token
from .forms import PasswordResetForm
from .forms import SetPasswordForm
from django.db.models.query_utils import Q
from .forms import FriendRequestForm, FriendForm
from .models import FriendRequest, Friend

# Function added to the url for Email confirmation


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("main:login")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("main:homepage")


# Function that sends the email
def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "template_activate_account.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f"Dear {user}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.",
        )
    else:
        message.error(
            request,
            f"Problem sending email to {to_email}, check if you typed it correctly.",
        )


# Main views


def homepage(request):
    # now if you're already authenticated you can't access base path
    if request.user.is_authenticated:
        return redirect("post:base")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                # return redirect("main:homepage")
                return redirect("post:base")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="main/home.html", context={"login_form": form}
    )


def register_request(request):
    if request.user.is_authenticated:
        return redirect("post:base")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get("email"))
            # return redirect("main:homepage")
            return redirect("main:login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="main/register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.user.is_authenticated:
        return redirect("post:base")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # return redirect("main:homepage")
                return redirect("post:base")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="main/login.html", context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:homepage")


# def password_reset_request(request):
#     form = PasswordResetForm()
#     return render(
#         request=request,
#         template_name="password_reset.html",
#         context={"form": form}
#         )

# def passwordResetConfirm(request, uidb64, token):
#     return redirect("main:homepage")


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["email"]
            associated_user = (
                get_user_model().objects.filter(Q(email=user_email)).first()
            )
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string(
                    "template_reset_password.html",
                    {
                        "user": associated_user,
                        "domain": get_current_site(request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        "token": account_activation_token.make_token(associated_user),
                        "protocol": "https" if request.is_secure() else "http",
                    },
                )
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, "Password reset email sent.")
                else:
                    messages.error(
                        request,
                        "Problem sending reset password email, <b>SERVER PROBLEM</b>",
                    )

            return redirect("main:homepage")

        # for key, error in list(form.errors.items()):
        #     if key == 'captcha' and error[0] == 'This field is required.':
        #         messages.error(request, "You must pass the reCAPTCHA test")
        #         continue

    form = PasswordResetForm()
    return render(
        request=request, template_name="password_reset.html", context={"form": form}
    )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Your password has been set. You may go ahead and <b>log in </b> now.",
                )
                return redirect("main:homepage")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, "Something went wrong, redirecting back to Homepage")
    return redirect("main:homepage")


def AddFriend(request):
    print("receiver")
    print(request.POST["receiver"])
    print("user")
    print(request.user)
    User = get_user_model()
    sender = User.objects.get(username=request.user)
    receiver = User.objects.get(username=request.POST["receiver"])
    friend_request_form = FriendRequestForm()
    new_friend_request = friend_request_form.save(False)
    new_friend_request.sender = sender
    new_friend_request.receiver = receiver
    new_friend_request.status = "pending"
    new_friend_request.save(True)
    redirect_str = "/home/profile/" + request.POST["receiver"]
    return redirect(redirect_str)


def DeleteFriend(request):
    User = get_user_model()
    deleted_friend = User.objects.get(username=request.POST["friend"])
    deleter = User.objects.get(username=request.user)
    FriendRequest.objects.filter(sender=deleted_friend, receiver=deleter).delete()
    FriendRequest.objects.filter(sender=deleter, receiver=deleted_friend).delete()
    Friend.objects.filter(primary=deleter, secondary=deleted_friend).delete()
    Friend.objects.filter(primary=deleted_friend, secondary=deleter).delete()
    return redirect(request.META.get("HTTP_REFERER"))


def AcceptFriend(request):
    print(request.POST["sender"])
    print(request.user)
    User = get_user_model()
    receiver = User.objects.get(username=request.user)
    sender = User.objects.get(username=request.POST["sender"])
    friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
    friend_request.status = "accepted"
    friend_request.save()

    try:
        Friend.objects.get(primary=sender, secondary=receiver)

    except Friend.DoesNotExist:
        print("friend doesn not exist")
        friend_form = FriendForm()
        new_friend = friend_form.save(False)
        new_friend.primary = sender
        new_friend.secondary = receiver
        new_friend.save(True)

        friend_form_secondary = FriendForm()
        new_friend_secondary = friend_form_secondary.save(False)
        new_friend_secondary.primary = receiver
        new_friend_secondary.secondary = sender
        new_friend_secondary.save(True)
    redirect_str = "/home/profile/" + str(request.user)
    return redirect(redirect_str)
