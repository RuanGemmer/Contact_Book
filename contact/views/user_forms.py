from django.shortcuts import render, redirect
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import auth


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado com sucesso')
            return redirect('contact:login')

    return render(
        request,
        'contact/register.html',
        {
            'form': form,
            'title': 'Register User'
        }
    )


def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'contact/register.html',
            {
                'form': form,
                'title': 'Update User'
            }
        )

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/register.html',
            {
                'form': form,
                'title': 'Update User'
            }
        )

    form.save()
    messages.success(request, 'Usuário atualizado com sucesso')
    return redirect('contact:login')


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            full_name = user.get_full_name().split(' ', 1)
            name = full_name[0].capitalize()
            auth.login(request, user)
            messages.info(request, f'Bem vindo, {name}!')
            return redirect('contact:index')

        messages.error(request,
                       'Erro ao fazer login. Usuário e/ou\
                              Senha incorreta(s)')

    return render(
        request,
        'contact/login.html',
        {
            'form': form,
            'title': 'Update User'
        }
    )


def logout_view(request):
    auth.logout(request)
    messages.info(request, 'Logout realizado com sucesso!')

    return redirect('contact:login')
