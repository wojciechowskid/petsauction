from .serializers import LotSerializer, BidSerializer, BidStatusSerializer
from .models import Lot, Bid
from rest_framework import exceptions, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.permissions import IsOwnerOrReadOnly


class LotViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Lot.objects.filter(status=Lot.active)


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_lot(self):
        return Lot.objects.get(pk=self.kwargs['lot_id'])

    def perform_create(self, serializer):
        lot = self.get_lot()
        if lot.owner == self.request.user or lot.status != Lot.active:
            raise exceptions.ValidationError('Wrong Lot id')
        serializer.save(
            author=self.request.user,
            lot=lot
        )

    def perform_update(self, serializer):
        lot = self.get_lot()
        if lot.status != Lot.active:
            raise exceptions.ValidationError('Bid belongs to inactive Lot')

    def get_queryset(self):
        return Bid.objects.filter(lot=self.kwargs['lot_id'])

    def get_serializer_class(self):
        if self.action in ['accept_bid']:
            return BidStatusSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def accept_bid(self, request, lot_id=None, pk=None):
        user = request.user
        lot = self.get_lot()
        bid = self.get_object()

        serializerClass = self.get_serializer_class()
        serializer = serializerClass(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 'Wrong bid status'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif lot.owner != user:
            return Response(
                {'status': 'Not permited to accept bids in lots of others'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif lot.status != Lot.active:
            return Response(
                {'status': 'Not allowd to accept bids in closed lots'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif bid.amount > bid.author.balance:
            return Response(
                {'status': 'Insufficient balance of the bidder'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            bid.status = Bid.accepted
            bid.save()
            lot.status = Lot.closed
            lot.save()
            lot.pet.owner = bid.author
            lot.pet.save()
            bid.author.balance = bid.author.balance - bid.amount
            bid.author.save()
            lot.owner.balance += bid.amount
            lot.owner.save()
            return Response({'status': 'bid accepted'})

