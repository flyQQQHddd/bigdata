"""
URL configuration for bigdata project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views
from . import api
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    # index 主页面
    path('', RedirectView.as_view(url='index/', permanent=True)),
    path('index/', views.index, name="index"),
    # 数据分析
    path('analysis/', views.analysis, name="analyzation"),
    #数据预测
    path('prediction/',views.prediction,name="prediction"),
    #报告
    path('report/',views.report,name="report"),
    #快速开始（上传）
    path('upload/',views.upload,name="upload"),
    #帮助与支持
    path('help/',views.help,name="help"),
    # 数据后台
    path('admin/', admin.site.urls),
    # API接口
    path('api/', api.api_base, name="api"),
    # 测试功能界面
    path('test/', views.test, name="test"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
