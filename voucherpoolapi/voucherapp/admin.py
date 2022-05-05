from django.contrib import admin

from .models import Customer, SpecialOffer, VoucherCode

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'customer', 'special_offer', 'used_at', 'is_used')
    search_fields=('customer__email',)

admin.site.register(Customer)
admin.site.register(SpecialOffer)
admin.site.register(VoucherCode, VoucherAdmin)
