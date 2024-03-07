from django.shortcuts import render, redirect
from authors.forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)
    context = {
        'form': form,
        'form_action': reverse('authors:register_create'),
    }
    return render(request, 'authors/pages/register_view.html', context=context)


def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        # commit=False -> serve para não salvar o form na base de dados de imediato
        # salvando a senha da maneira correta
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in')
        del request.session['register_form_data']
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    context = {
        'form': form,
        'form_action': reverse('authors:login_create')
    }
    return render(request, 'authors/pages/login.html', context=context)


def login_create(request):
    if not request.POST:
        raise Http404

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'You are logged in.')
            login(request, authenticated_user)

        else:
            messages.error(request, 'Invalid credentials.')
    else:
        messages.error(request, 'Invalid username or password')
    return redirect(login_url)


# redirect_field_name recebe a página que o usuário tentou acessar antes de estar logado, assim, ele será redirecionado para a página diretamente
# esse atributo é passado para a url
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        return redirect('authors:login')

    logout(request)
    return redirect('authors:login')