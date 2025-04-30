from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Document
from .serializers import DocumentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    pass


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.request.query_params.get('tag_id', None)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        sort_by = self.request.query_params.get('sort', 'created_at')
        return queryset.order_by(sort_by)
