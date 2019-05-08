from django.urls import path
from . import views


urlpatterns = [
    path('', views.SettingView.as_view(), name='setting'),
]
