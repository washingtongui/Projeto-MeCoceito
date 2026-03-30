from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from backend.admin import custom_admin_site as admin

urlpatterns = [
    path('admin/', admin.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
