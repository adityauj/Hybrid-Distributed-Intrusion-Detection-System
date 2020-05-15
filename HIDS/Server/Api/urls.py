from django.urls import path
from . import views 

urlpatterns = [
	path('',views.index,name = 'index'),
    path('ip',views.getIP, name='getIP'),
    path('attack',views.attack,name ='attack'),
]
