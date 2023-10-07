from django.urls import path
from .views import *


urlpatterns = [
    path("clients", Clients.as_view(), name="clients"),
    path("clients/<int:id>", ClientInformation.as_view(), name="client_information")
]