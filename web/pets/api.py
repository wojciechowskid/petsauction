from .serializers import PetSerializer
from .models import Pet
from rest_framework import viewsets
from rest_framework import permissions
from utils.permissions import IsOwnerOrReadOnly


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
