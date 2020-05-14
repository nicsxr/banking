from django.contrib import admin
from django.urls import path

from .views import home

from accounts.views import login_view, register_view, logout_view, dashboard_view, send_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', login_view),
    path('register/', register_view),
    path('logout/', logout_view),
    path('dashboard/', dashboard_view),
    path('dashboard/send', send_view),
]