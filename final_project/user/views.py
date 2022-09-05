from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user=authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
            return HttpResponseRedirect('/')				
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)						
    return HttpResponseRedirect("/")

# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required(login_url="/login/")
def user_list_view(request):
    users=User.objects.all()
    paginator = Paginator(users,3)
    page= request.GET.get('page')
    users=paginator.get_page(page)
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    return render(request, "users.html", {"users": users})
