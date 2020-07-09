from rest_framework import permissions, viewsets, mixins, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from utils.permissions import IsOwnerOrReadOnly

from .serializers import (AuctionUserSerializer,
                          BalanceSerializer,
                          CreateAuctionUserSerializer,
                          PasswordSerializer)

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    queryset = UserModel.objects.all()
    serializer_class = AuctionUserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [permissions.AllowAny,]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateAuctionUserSerializer
        return super().get_serializer_class()


class UpdateBalanceView(UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = UserModel.objects.all()
    serializer_class = BalanceSerializer


class UpdatePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, pk=None, *args, **kwargs):
        self.object = UserModel.objects.get(pk=pk)
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password"]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
