
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from .views import GenerateTextImageView


urlpatterns = [
  path('aipost', GenerateTextImageView.as_view(), name="create_ai"), 
]
