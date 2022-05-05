from django.urls import path, include

from rest_framework import routers

from .views import CustomerViewSet, \
    RedeemApiView, SpecialOfferViewSet, \
    VoucherCodeViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'offers', SpecialOfferViewSet)
router.register(r'vouchers', VoucherCodeViewSet)

url_patterns = [
    path('redeem', RedeemApiView.as_view())
]

url_patterns += router.urls
