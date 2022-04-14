from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile

from .forms import LoginForm, UserRegistrationForm,UserEditForm, ProfileEditForm
from django.contrib import messages


def user_login(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario Autenticado Exitosamente')
                else:
                    return HttpResponse('Cuenta deshabilitada')
            else:
                return HttpResponse('Login inválido')
    else:
        form = LoginForm()

    return render(
        request,
        'cuenta/login.html',
        {
            'form':form,

        }
    )

@login_required
def deshboard(request):
    return render(
        request,
        'cuenta/dashboard.html', 
        {
            'section': 'dashboard',
        }
    )

def register(request):
    if(request.method == 'POST'):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password']
            )

            password2 = user_form.cleaned_data['password2']

            password1 = user_form.cleaned_data['password']

            if password1 != password2:
                messages.error(
                request,
                'Las contraseñas son diferentes, No puedes crear tu cuenta'
                )
                user_form = UserRegistrationForm()
                 
            else:
                new_user.save()
                Profile.objects.create(user=new_user)

                return render(
                    request,
                    'cuenta/register_done.html',
                    {
                        'new_user': new_user,
                    }
                )
    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        'cuenta/register.html',
        {
            'user_form': user_form,
        }

    )

@login_required
def edit(request):

    if request.method == 'POST':

        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )

        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                'El perfil se ha actualizado de manera exitosa'
            )
        
        else:
            messages.error(
                request,
                'El perfil no se ha actualizado de manera exitosa'
            )

    else:

        user_form = UserEditForm(
            instance=request.user
        )

        profile_form = ProfileEditForm(
            instance=request.user.profile
        )
    
    return render(
        request,
        'cuenta/edit.html',
        {
            'user_form':user_form,
            'profile_form':profile_form,
        }
    )