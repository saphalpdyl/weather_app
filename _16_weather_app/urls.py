from django.contrib import admin
from django.urls import path

from weather_app.views import MainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main' )
]
