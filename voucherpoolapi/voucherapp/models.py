from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

class Customer(models.Model):
    '''
    Customer model
    '''
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.email}"


class SpecialOffer(models.Model):
    '''
    SpecialOffer model
    '''
    name = models.CharField(max_length=100)
    discount = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self) -> str:
        return f"{self.name} - {self.discount}% OFF"


class VoucherCode(models.Model):
    '''
    VoucherCode model
    '''
    code = models.CharField(max_length=16, validators=[
                            MinLengthValidator(8)], unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    special_offer = models.ForeignKey(SpecialOffer, on_delete=models.CASCADE)
    expiry = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # only voucher for one customer and special offer allowed
        unique_together = (('customer', 'special_offer'),)

    def __str__(self) -> str:
        return self.code