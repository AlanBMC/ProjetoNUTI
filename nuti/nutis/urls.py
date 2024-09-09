from django.urls import path
from . import views
from .views import HomeAPIView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Documentação da API",
      terms_of_service="https://www.seusite.com/terms/",
      contact=openapi.Contact(email="contato@seusite.com"),
      license=openapi.License(name="Licença MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
#Rotas - foi criado apenas um rota padrão.
    path('', views.home, name='index'),
    path('api/home/', HomeAPIView.as_view(), name='api-home'),

     # Swagger routes
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # ReDoc route
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]