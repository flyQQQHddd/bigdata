from django.http import HttpResponse
from django.shortcuts import render


def test(request):
    context          = {}
    context['hello'] = 'Hello Echarts!'
    return render(request, 'test.html', context)


def index(request):

    return render(request, 'index.html')


def analyzation(request):

    return render(request, 'inner-page.html')