from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('Users.urls', namespace='Users')),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # documentations
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    #path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
