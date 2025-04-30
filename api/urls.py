from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, LoginView

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('users/<int:id>/login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
