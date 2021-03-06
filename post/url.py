from django.urls import path
from . import views


urlpatterns = [
    path('<int:post_id>', views.PostView.as_view(), name='post'),
    path('<str:id>/make_read/<int:notification_id>/<str:t>', views.MakeReadView.as_view(), name='make_read'),
    path('getComment', views.CommentView.as_view(), name='comment'),
    path('getReply', views.ReplyView.as_view(), name='reply'),
]
