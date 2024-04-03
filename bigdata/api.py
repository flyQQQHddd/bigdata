from django.http import HttpResponse
from django.shortcuts import render
import json

def api_base(request):

    print(request)

    # 准备数据
    categories = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    data = [5, 20, 36, 10, 10, 20]

    result = {
        "message": 'success', 
        "status": '200', 
        "data": {
            "categories": categories,
            "data": data
        }
        }

    # 转换为 JSON 字符串并返回
    return HttpResponse(json.dumps(result), content_type="application/json")




