
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    #url to access to AI
    path('ai/', include('aiapp.urls')),
]
