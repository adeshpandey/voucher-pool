from django_filters import FilterSet, CharFilter

from .models import VoucherCode

class EmailFilterSet(FilterSet):
    email = CharFilter(
        field_name='customer__email')

    class Meta:
        model = VoucherCode
        fields = ['email']
