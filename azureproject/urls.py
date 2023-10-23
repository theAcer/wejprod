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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
admin.site.site_header = "Wejja Golf admin"
admin.site.site_title = "Wejja Golf admin site"
admin.site.index_title = "Wejja Golf Admin"

if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns