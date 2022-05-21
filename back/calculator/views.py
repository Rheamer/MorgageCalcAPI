from rest_framework import generics, viewsets, mixins
from rest_framework import permissions
from rest_framework.response import Response
from .models import Offer
from .serializers import OfferSerializer
from .filters import OfferFilter
from django_filters import rest_framework as filters
from .utils import get_payment, append_payment


class OfferDetailApiView(viewsets.GenericViewSet,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_field = 'id'


class OfferApiView(viewsets.ReadOnlyModelViewSet,
                   mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OfferFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        order = request.GET.get('order', '')
        if 'rate' == order or '-rate' == order:
            order += "_min"
            queryset = queryset.order_by(order)

        price = request.GET.get('price', '')
        term = request.GET.get('term', '')
        deposit = request.GET.get('deposit', '')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            try:
                append_payment(serializer.data, price, term, deposit, order)
            except ValueError as e:
                pass
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        try:
            append_payment(serializer.data, price, term, deposit, order)
        except ValueError as e:
            pass
        return Response(serializer.data)
