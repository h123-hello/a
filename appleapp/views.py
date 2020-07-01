from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from rest_framework.renderers import BrowsableAPIRenderer

from rest_framework.views import APIView

from appleapp.models import User
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

'''
function base view 基于函数定义的视图
class base view 基于类定义的视图
'''


# Create your views here.
@csrf_exempt
def user(request):
    if request.method == "CET":
        # username = request.GET.get("username")
        print("GET SUCCESS 查询")
        return HttpResponse("GET SUCCESS")

    elif request.method == "POST":
        # username = request.POST.get("username")
        print("POST SUCCESS 添加")
        return HttpResponse(" POST SUCCESS")

    elif request.method == "DELETE":
        # username = request.POST.get("username")
        print("DELETE SUCCESS 删除")
        return HttpResponse(" DELETE SUCCESS")

    elif request.method == "PUT":
        # username = request.PUT.get("username")
        print("PUT SUCCESS 修改")
        return HttpResponse(" PUT SUCCESS")


@method_decorator(csrf_exempt, name="dispatch")  # 让类视图免除csrf认证
class UserView(View):
    def get(self, request, *args, **kwargs):
        # 可以通过_request:访问对象
        # print("GET SUCCESS 查询")
        user_id = kwargs.get("id")
        if user_id:
            user_val = User.objects.filter(pk=user_id).values("username", "password", "gender").first()
            if user_val:
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_val
                })
        else:
            user_list = User.objects.all().values("username", "password", "gender")
            print(type(user_list))
            if user_list:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": "list(user_list)",
                })
        return JsonResponse({
            "status": 500,
            "message": "查询失败",
        })

        # print(user_id)
        return HttpResponse("GET SUCCESS")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            user_obj = User.objects.create(username=username, password=pwd)
            return JsonResponse({
                "status": 201,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "gender": user_obj.gender}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建失败"
            })
        # print("POST SUCCESS 添加")
        return HttpResponse("POST SUCCESS")

    def PUT(self, request, *args, **kwargs):
        print("PUT SUCCESS 修改")
        return HttpResponse("PUT SUCCESS")

    def DELETE(self, request, *args, **kwargs):
        print("DELETE SUCCESS 删除")
        return HttpResponse("DELETE SUCCESS")


# 开发基于drf的视图
class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # print("DRF GET VIEW")
        # print(request._request.GET)
        print(request.GET)
        print(request.query_params)
        user_id = kwargs.get("pk")

        return Response("DRF GET SUCCESS")

    def post(self, request, *args, **kwargs):
        # print("POST GET VIEW")
        # post请求传递参数的形式 form-data www-urlencoded json

        # print(request._request.POST)  # Django 原生的request对象
        print(request.POST)  # DRE 封装后的 request对象
        print(request.data)
        # 可以获取多种格式的参数 DRF 扩展的请回去参数 兼容性最强
        return Response("POST GET SUCCESS")


class UserAPI(APIView):
    # 单独为某个视图指定渲染器  局部使用
    # 局部的要比全局的优先级高
    renderer_classes = (BrowsableAPIRenderer,)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        print(request.query_params)
        return Response("user_id")







class StudentAPIView(APIView):
    # 局部使用解析器
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print("POST方法")

        # print(request.POST)
        print(request.data)

        return Response("POST方法访问成功")




