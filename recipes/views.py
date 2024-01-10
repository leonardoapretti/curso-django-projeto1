from django.shortcuts import render


def home(request):
    context = {
        'name': 'Leonardo',
    }
    return render(request, 'recipes/pages/home.html', context=context)
