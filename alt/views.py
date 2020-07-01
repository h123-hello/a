from abc import ABC

import kwargs as kwargs
from django.shortcuts import render
from rest_framework import serializers
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from alt.models import Employee
from .serializers import EmployeeSerializer

class EmployeeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        if user_id:
            # 查询单个
            emp_obj = Employee.objects.get(pk=user_id)
            # 查询出的单个的员工对象无法直接序列化，需要使用序列化器完成序列化
            # .data 将序列化器的数据打包成字典
            emp_ser = EmployeeSerializer(emp_obj).data

            return Response({
                "status": 200,
                "msg": "查询单个员工成功",
                "results": emp_ser,
            })
        else:
            #            #查询所有
            # 员工对象无法直接序列化返回到前台
            emp_list = Employee.objects.all()
            emp_list_ser = EmployeeSerializer(emp_list, many=True).data

            return Response({
                "status": 200,
                "mag": "查询所有员成功",
                "results": emp_list_ser
            })

    def post(self,request, *args,**kwarge):
        user_data = request.data
        if not isinstance(user_data,dict) or user_data == {}:
            return Response({
                "status":501,
                "msg":"数据有误",
            })

        serializer = EmployeeSerializer(data=user_data)

        if serializer.is_valid():
            emp_obj = serializer.save()
            print(emp_obj,"this is obj",type(emp_obj))

            return Response({
                "status":201,
                "msg" : "用户创建成功",
                "results" : EmployeeSerializer(emp_obj).data
            })
        else:
            return Response({
                "status" : 501,
                "msg" : "用户创建失败",
                "results":serializer.errors
            })
