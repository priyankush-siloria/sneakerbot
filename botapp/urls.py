from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', DiscordLoginView.as_view(), name="login"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),

]
