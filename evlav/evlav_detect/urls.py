from django.urls import path

from .views import IndexView
from .views import AboutView
from .views import ToolsView
from . import views

urlpatterns = [
  path('', IndexView.as_view(), name="index"),
  path('upload/', views.upload, name="upload"),
  path('about/', AboutView.as_view(), name="about"),
  path('tools/', ToolsView.as_view(), name="tools"),
  path('tools_result/', views.tools_upload, name="tools_result")
]
