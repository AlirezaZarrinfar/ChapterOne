from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('Users.urls', namespace='Users')),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # documentations
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    #path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
