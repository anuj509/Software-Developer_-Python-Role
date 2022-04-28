from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('home/',views.router, name='router'),
    path('routers/', views.RouterMain.as_view(), name='routers'),
    path('router/<str:ip>/', views.RouterDetail.as_view(), name='routerdetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
