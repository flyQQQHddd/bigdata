from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
# import paramiko
import time
from . import clean_collection
import os
import glob
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def count_csv_files(path):
    # 获取指定路径下所有的CSV文件
    csv_files = glob.glob(os.path.join(path, '*.csv'))
    # 判断CSV文件数量是否为9
    if len(csv_files) == 9:
        return True
    else:
        return False

def test(request):
    context          = {}
    context['hello'] = 'Hello Echarts!'
    return render(request, 'test.html', context)

#首页
def index(request):
    return render(request, 'index.html')

#课程评估
def curriculum(request):
    # 指定要检查的路径
    path = '/root/Desktop/data/'
    # 检查用户是否已经上传了文件
    if count_csv_files(path):
        # 用户已经上传了文件，渲染curriculum.html页面
        return render(request, 'curriculum.html')
    else:
        # 用户还没有上传文件，返回一个提示信息
        return HttpResponse('<script>alert("请先上传数据"); window.location.href="/upload/";</script>')

#用户分析
def user(request):
   # 指定要检查的路径
    path = '/root/Desktop/data/'
    # 检查用户是否已经上传了文件
    if count_csv_files(path):
        # 用户已经上传了文件，渲染curriculum.html页面
        return render(request, 'user.html')
    else:
        # 用户还没有上传文件，返回一个提示信息
        return HttpResponse('<script>alert("请先上传数据"); window.location.href="/upload/";</script>')

#个性推荐
def personalized(request):
   # 指定要检查的路径
    path = '/root/Desktop/data/'
    # 检查用户是否已经上传了文件
    if count_csv_files(path):
        # 用户已经上传了文件，渲染curriculum.html页面
        return render(request, 'personalized.html')
    else:
        # 用户还没有上传文件，返回一个提示信息
        return HttpResponse('<script>alert("请先上传数据"); window.location.href="/upload/";</script>')

#资源优化
def resource(request):
   # 指定要检查的路径
    path = '/root/Desktop/data/'
    # 检查用户是否已经上传了文件
    if count_csv_files(path):
        # 用户已经上传了文件，渲染curriculum.html页面
        return render(request, 'resource.html')
    else:
        # 用户还没有上传文件，返回一个提示信息
        return HttpResponse('<script>alert("请先上传数据"); window.location.href="/upload/";</script>')


@csrf_exempt
#快速开始（上传界面）
def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)  # 拼装目录名称+文件名称
        print(file_path)
        with open(file_path, 'wb+') as destination:  # 写文件word
          for chunk in file.chunks():
            destination.write(chunk)
            
            #clean_collection.wash_file(file_path,file.name)

        return JsonResponse({
            'status': 'success',
            'file_path': file_path,
            'message': 'File uploaded successfully.'
        })  
            
    return render(request, 'upload.html')



#帮助与支持
def help(request):

    return render(request,'help.html')
