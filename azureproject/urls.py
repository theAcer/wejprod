"""azureproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework_swagger.views import get_swagger_view

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="WEJJA API",
        default_version='v1',
        description="Test API ",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
)

urlpatterns = [
    #path('', include('restaurant_review.urls')),
    path('admin/', admin.site.urls),
    # User management
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    
    # Local apps
    path('accounts/', include('users.urls')),
    path('party/', include('party.urls', namespace='party')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('games/', include('games.urls', namespace='games')),
    path('tournaments/', include('tournaments.urls', namespace='tournaments')),
    path('', include('dashboard.urls')),
    path('api/', include('rest_framework.urls')),
    path('friends/', include('friendship.urls', namespace='friends')),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]


# If you also want to add the URL for the ReDoc interface, you can do so like this:
urlpatterns += [
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
admin.site.site_header = "Wejja Golf admin"
admin.site.site_title = "Wejja Golf admin site"
admin.site.index_title = "Wejja Golf Admin"

if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns