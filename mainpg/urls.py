from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'mainpg'
urlpatterns = [
    path('geo', views.GeoView.as_view(), name='geo'),
    path('telep', views.TeleportView.as_view(), name='telep'),
    path('telepadd', views.TeleportaddView.as_view(), name='telepadd'),
    path('add1', views.Teleportadd1View.as_view(), name='add1'),
    path('gplace', views.GplaceView.as_view(), name='gplace'),
    path('test', views.TestView.as_view(), name='test'),
]