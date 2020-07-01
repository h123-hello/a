from rest_framework import serializers, exceptions

from alt.models import Employee
from banana import settings


class EmployeeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=8,
        min_length=4,
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了",
        }
    )
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()
    phone = serializers.CharField()
    # 自定义字段 重复密码
    re_pwd = serializers.CharField()

    # TODO 在create方法保存之前，DRF提供了两个钩子函数对数据进行效验

    # 局部效验钩子:可以对反序列化中某个字段进行效验
    def validate_username(self, value):

        # 自定义用户名效验规则

        if "1" in value:
            raise exceptions.ValidationError("用户名错误")
        return value

    # 全局效验钩子 可以通过attrs获取到前台发送所有的参数
    def validate(self, attrs):
        # 可以对前端发送的所有数据进行自定义效验
        # print(self,"当前实例所使用的反序列化器")
        pwd = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        # 自定义规则 两次密码如果不一致 则无法保存

        if pwd != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")
        return attrs

    # 想要完成新增员工 必须重写 create()方法
    # 继承的serializer类并没有新增做具体的实现
    def create(self, validated_data):
        # 方法完成新增
        return Employee.objects.create(**validated_data)

    def create(self, validated_data):
        print(validated_data)
        return Employee.objects.create(**validated_data)

    # 自定义字段 返回盐 使用SerializerMethodField来定义

    salt = serializers.SerializerMethodField()

    def get_salt(self, obj):
        return "salt"

    # 自定义返回值

    gender = serializers.SerializerMethodField()

    # self 是当前序列器 obj是对象

    def get_gender(self, obj):
        # print(obj,gender,type(obj))
        # 性别是choices类别 get_字段名_display()直接访问值
        return obj.get_gender_display()

    # 定义返回图片路径的全部路径
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        return "%s%s%s" % ("http//127.0.0.1:8000", settings.MEDIA_ROOT, str(obj.pic))

