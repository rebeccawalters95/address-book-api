from django.urls import include, path
from rest_framework import routers
from . import views

# Registering the addresses api
router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet)

urlpatterns = [
    # endpoint of http://127.0.0.1:8000/address/ is protected by authentication.
    # Expect to return "detail": "Authentication credentials were not provided."
    # if user is not authorised, and should list all addresses available if user is authorised
    path('', include(router.urls)),
    # endpoint of http://127.0.0.1:8000/register allows users to register with an email, name, and password. They can
    # then use their email and password to login using login button top right hand corner OR by navigating to
    # http://127.0.0.1:8000/api-auth/login/?next=/addresses/
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
