from django.shortcuts import render, redirect
from . forms import RegisterForm
from django.http import Http404
from django.contrib import messages


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)
    context = {
        'form': form,
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
        form.save()
        # data.outro_campo -> serve para adcionar campos ao formulário
        # manda mensagem de sucesso para o usuário
        messages.success(request, 'Your user is created, please log in')

        del request.session['register_form_data']

    return redirect('authors:register')
