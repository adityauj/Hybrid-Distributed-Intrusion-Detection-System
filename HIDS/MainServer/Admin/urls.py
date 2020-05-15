from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('ip/',views.home,name="home"),
    path('logs',views.write_logs,name='write_logs'),
    path('get',views.getTextFile,name="getTextFile"),
    path('draw',views.doughnut_data,name="doughnut_data"),
    path('attack',views.attack,name="attack"),
]