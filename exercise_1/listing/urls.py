from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('routers/', views.RouterMain.as_view(), name='routers'),
    path('router/<int:id>/', views.RouterDetail.as_view(), name='routerdetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
