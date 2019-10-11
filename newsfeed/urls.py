from django.urls import path
from . import views, ajax_response


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('create', views.CreatePostView.as_view(), name='create'),
    path('search', views.SearchView.as_view(), name='search'),
    path('saved', views.SavedView.as_view(), name='saved'),
    path('notification', views.NotificationView.as_view(), name='notification'),
    path('tag/<str:name>', views.TagPostView.as_view(), name='tag-post'),
    path('ajax', ajax_response.response, name='ajax'),
    path('getPopupNotification', views.NotificationPopupView.as_view(), name='popup-notification'),

]
