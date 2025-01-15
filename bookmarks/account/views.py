from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request,
                  'account/login.html',
                  {'form': form})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)  # создание нового объекта пользователя, но пока не сохранять его
            new_user.set_password(user_form.cleaned_data['password'])  # сохранение шифрованного пароля
            new_user.save()
            Profile.objects.create(user=new_user)  # добавление и связывание модели Profile с новым пользователем
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form,
                  })


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})
