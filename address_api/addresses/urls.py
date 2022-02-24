from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
