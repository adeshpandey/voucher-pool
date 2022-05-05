from datetime import datetime
from enum import unique
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Customer, SpecialOffer, VoucherCode
from .couponcode import couponcode


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'email')


class SpecialOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffer
        fields = ('name', 'discount')


class VoucherCodeSerializer(serializers.ModelSerializer):
    """
    ``Serializer`` for ``VoucherCode`` ..
    """
    special_offer_name = serializers.ReadOnlyField(source="special_offer.name")

    class Meta:
        model = VoucherCode
        fields = ('code', 'expiry', 'is_used', 'used_at',
                  'special_offer_name', 'customer', 'special_offer',)
        read_only_fields = ('code', 'is_used', 'used_at', 'special_offer_name')
        extra_kwargs = {'customer': {'write_only': True},
                        'special_offer': {'write_only': True}}

    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        if(self.instance is None):
            kwargs["code"] = couponcode.generate(8)
        return super().save(**kwargs)


class RedeemSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    code = serializers.CharField(required=True, allow_blank=False)


class VoucherCodeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherCode
        fields = ('code', 'customer', 'special_offer',
                  'expiry', 'is_used', 'used_at')
