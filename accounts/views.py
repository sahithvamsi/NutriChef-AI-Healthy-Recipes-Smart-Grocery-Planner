from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home_v(request):
    return render(request, "accounts/home.html")


def login_v(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")   # ✅ STAY ON SAME HOME
        else:
            return render(request, "accounts/login.html",
                          {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")


def sign_v(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            User.objects.create_user(username=username, password=password1)
            return redirect("login")
        else:
            return render(request, "accounts/signup.html",
                          {"error": "Passwords do not match"})

    return render(request, "accounts/signup.html")


def logout_v(request):
    logout(request)
    return redirect("home")


# ❌ REMOVE dashboard_v completely
# delete this:
# @login_required
# def dashboard_v(request):
#     return render(request, 'accounts/dashboard.html')


def blog1(request):
    return render(request, "accounts/blog1.html")


def blog2(request):
    return render(request, "accounts/blog2.html")


def blog3(request):
    return render(request, "accounts/blog3.html")


def blog4(request):
    return render(request, "accounts/blog4.html")
from django.contrib.auth.decorators import login_required

@login_required
def my_saved_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, "accounts/saved_recipes.html",
                  {"recipes": recipes})