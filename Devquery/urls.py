from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('newsfeed.urls')),
    path('post/', include('post.url')),
    path('profile/', include('profilesection.url')),
    path('account/', include('account.urls')),
    path('setting/', include('settingsection.url')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
