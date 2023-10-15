from django.urls import path
from .views import (home)

app_name = "core1"

urlpatterns = [
    path('', home, name='home'),

]

