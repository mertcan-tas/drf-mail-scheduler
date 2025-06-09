from django.contrib import admin
from django.urls import path,re_path, include
from decouple import config
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from schema_graph.views import Schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('app.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("schema/", Schema.as_view()),
]

urlpatterns.append(path('', include('testing.urls'))) if config("DEBUG", default=False, cast=bool) else None

