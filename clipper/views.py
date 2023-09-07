from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q, Count
from dal import autocomplete
from taggit.models import Tag


from .forms import AddClipForm, EditClipForm

from .models import User, Clip


def index(request):
    return render(request, "clipper/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "clipper/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "clipper/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "clipper/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "clipper/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "clipper/register.html")


@login_required(login_url="/login/")
def account(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed.")
            return redirect("account")
        else:
            messages.error(request, "Invalid password.")
            return redirect("account")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "clipper/account.html", {"form": form})


@login_required(login_url="/login/")
def add_clip(request):
    if request.method == "POST":
        form = AddClipForm(request.POST)
        if form.is_valid():
            clip = form.save(commit=False)
            clip.user = request.user
            clip.save()
            form.save_m2m()
            return redirect("edit", clip.id)
    elif request.method == "GET":
        form = AddClipForm(request.GET, initial={"user": request.user})
        if form.is_valid():
            clip = form.save(commit=False)
            clip.user = request.user
            clip.save()
            form.save_m2m()
            return redirect("edit", clip.id)
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("dashboard")


@login_required(login_url="/login/")
def new(request):
    form = AddClipForm()
    return render(request, "clipper/add.html", {"form": form})


@login_required(login_url="/login/")
def edit_clip(request, clip_id):
    clip = Clip.objects.get(id=clip_id)
    if clip.user != request.user:
        messages.error(request, "No access.")
        return redirect("dashboard")
    if request.method == "POST":
        form = EditClipForm(request.POST, instance=clip)
        if form.is_valid():
            clip = form.save(commit=False)
            clip.save()
            form.save_m2m()
            return redirect("dashboard")
    else:
        form = EditClipForm(instance=clip)
    return render(request, "clipper/clip.html", {"form": form, "clip": clip})


@login_required(login_url="/login/")
def dashboard(request):
    if "q" in request.GET:
        query = request.GET.get("q")
        user_clips = Clip.objects.filter(user=request.user).filter(
            Q(title__icontains=query)
            | Q(url__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        )
    elif "tag" in request.GET:
        tag_name = request.GET.get("tag")
        user_clips = Clip.objects.filter(user=request.user).filter(
            tags__name__in=[tag_name]
        )
    else:
        user_clips = Clip.objects.filter(user=request.user)

    user_tags = (
        Tag.objects.filter(
            clip__user=request.user,
        )
        .annotate(tag_count=Count("clip"))
        .order_by("-tag_count")
    )

    paginator = Paginator(user_clips, 12)

    page_number = request.GET.get("page")
    clips = paginator.get_page(page_number)

    return render(
        request,
        "clipper/dashboard.html",
        {"clips": clips, "tags": user_tags},
    )


def about(request):
    scheme = request.scheme
    host = request.get_host()
    return render(request, "clipper/about.html", {"host": f"{scheme}://{host}"})


@login_required(login_url="/login/")
def delete(request, clip_id):
    clip = Clip.objects.get(id=clip_id)
    if clip.user != request.user:
        messages.error(request, "No access.")
        return redirect("dashboard")
    clip.delete()
    return redirect("dashboard")
