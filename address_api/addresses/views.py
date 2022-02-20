from django.shortcuts import render
from rest_framework import viewsets

from .serializers import AddressSerializer
from .models import Address

# Create your views here.
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
