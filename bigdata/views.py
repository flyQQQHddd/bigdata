from django.http import HttpResponse
from django.shortcuts import render


def test(request):
    context          = {}
    context['hello'] = 'Hello Echarts!'
    return render(request, 'test.html', context)

#首页
def index(request):

    return render(request, 'index.html')

#数据分析
def analysis(request):

    return render(request, 'analysis.html')

#快速开始（上传界面）
def upload(request):

    return render(request, 'upload.html')

#预测
def prediction(request):

    return render(request,'prediction.html')

#报告
def report(request):

    return render(request,'report.html')

#帮助与支持
def help(request):

    return render(request,'help.html')
