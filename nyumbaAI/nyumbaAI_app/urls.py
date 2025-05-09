from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "nyumbaAI_app"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("chat/", views.chat, name="chat"),
]
# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
