from django.shortcuts import render, redirect
from authors.forms import RegisterForm, LoginForm, AuthorRecipeForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from utils.pagination import make_pagination
from django.utils.text import slugify
from django.utils.crypto import get_random_string
import os

PER_PAGE = os.environ.get('PER_PAGE', 6)


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
    if request.user.is_authenticated:
        return redirect('authors:dashboard')

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
    return redirect('authors:dashboard')


# redirect_field_name recebe a página que o usuário tentou acessar antes de estar logado, assim, ele será redirecionado para a página diretamente
# esse atributo é passado para a url
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request.')
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user.')
        return redirect('authors:login')

    messages.success(request, 'Logged out successfully.')
    logout(request)
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user,
    ).order_by('-created_at')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        'recipes': page_obj,
        'pagination_range': pagination_range,
    }

    return render(request, 'authors/pages/dashboard.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Your recipe has been updated!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    context = {
        'recipe': recipe,
        'form': form,
    }

    return render(request, 'authors/pages/dashboard_recipe.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    form = AuthorRecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.slug = slugify(recipe.title)
        exist_slug = Recipe.objects.filter(slug=recipe.slug).first()
        if exist_slug is not None:
            recipe.slug += get_random_string(length=4)
        recipe.save()

        messages.success(
            request, 'Your recipe has been created! Update it if you need.')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))

    context = {
        'form': form,
        'form_action': reverse('authors:dashboard_recipe_create')
    }

    return render(request, 'authors/pages/dashboard_recipe.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    recipe.delete()
    messages.success(request, 'The recipe has been deleted')

    return redirect(reverse('authors:dashboard'))
