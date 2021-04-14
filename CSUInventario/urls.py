from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('api/1.0/', include('rest.urls')),
    path('gestion/', include('Application.urls')),
    path('api-rest/', include('rest.urls')),
    path('rest-auth/', include('rest_auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
