from django.urls import path

from appleapp import views

urlpatterns = [
    path('user/',views.UserView.as_view()),
    path("users/<str:id>/",views.UserView.as_view()),
    path("api_user/",views.UserAPIView.as_view()),
    path("apil_user/<str:pk>/",views.UserAPI.as_view()),
    path("apie_user/",views.StudentAPIView.as_view()),
]