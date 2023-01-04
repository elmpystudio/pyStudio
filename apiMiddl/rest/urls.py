from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from oauth2_provider.decorators import protected_resource
from django.http import HttpResponse
import json
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = 'Administration'

swagger_schema_info = {
    "public": True,
    "permission_classes": (permissions.AllowAny,)
}

# swagger_schema_info['url'] = settings.SWAGGER_BASE_URL

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ), **swagger_schema_info)


@protected_resource()
def get_user(request):
    user = request.user
    return HttpResponse(
        json.dumps({
            'username': user.username,
            # 'email': user.email
        }),
        content_type='application/json')


urlpatterns = [

    path("oauth/", include('oauth2_provider.urls', namespace='oauth2_provider')),

    path("api/", include([

        path('ml/', include('ml_studio.urls')),
        path('whoami/', get_user),
        path('datasets/', include('datasets.urls')),
        path('', include('accounts.urls')),
        # no tableu licence then no need
        # path('tableau/', include('tableau.urls')),
        path('marketplace/', include('marketplace.urls')),
        path('jupyterhub/', include('jupyterhub.urls')),
        path('ml_models/', include('ml_models.urls')),
        path('notifications/', include('notifications.urls')),


        # django browsable api, probably will be deleted
        path('api/', include('rest_framework.urls', namespace='rest_framework')),

        # jwt tokens
        path('token/', jwt_views.TokenObtainPairView.as_view(),
             name='token_obtain_pair'),
        path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
             name='token_refresh'),

        # django admin
        path("admin/", admin.site.urls),

        # # swagger
        # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
