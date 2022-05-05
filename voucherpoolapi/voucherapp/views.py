from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.exceptions import bad_request
from rest_framework.views import Response
from datetime import datetime

from .filters import EmailFilterSet

from .models import Customer, SpecialOffer, VoucherCode
from .serializers import CustomerSerializer, RedeemSerializer, SpecialOfferSerializer, VoucherCodeSerializer, VoucherCodeWriteSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    '''
    API to manage customers
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SpecialOfferViewSet(viewsets.ModelViewSet):
    ''''
    API to manage the special offers
    '''
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferSerializer

class VoucherCodeViewSet(viewsets.ModelViewSet):
    '''
    API to manage vouchers
    Problem statement 1 and 3 is fulfilled here
    '''
    queryset = VoucherCode.objects.all()
    serializer_class = VoucherCodeSerializer
    filter_class = EmailFilterSet


class RedeemApiView(generics.CreateAPIView):
    '''
    API to redeem the voucher
    problem statement 2 is fulfilled here
    '''
    queryset = VoucherCode.objects.all()
    serializer_class = RedeemSerializer

    def create(self, request):

        if(self.get_serializer(data=request.data).is_valid(raise_exception=True)):
            try:

                instance = VoucherCode.objects.filter(customer__email=request.data.get(
                    'email'), code=request.data.get('code')).get()
                if(instance.is_used):
                    return Response({"detail": "already redeemed"}, 400)
                    
                serializer = VoucherCodeWriteSerializer(
                    instance, data={'is_used': True, 'used_at': datetime.now() }, partial=True)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "voucher redeemed successfully", "discount": instance.special_offer.discount}, 204)
                else:
                    return Response({"detail": "invalid request"}, 400)
            except VoucherCode.DoesNotExist:
                return Response({"detail": "invalid request"}, 400)
