from datetime import datetime
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Customer, SpecialOffer, VoucherCode


class CustomerTestCase(TestCase):
    '''
    TestCustomer model
    '''
    def setUp(self):
        """
        Create a new customer before each test cases
        """
        Customer.objects.create(name="adesh", email="adesh.pandey10@gmail.com")

    def test_customer_has_email(self):
        '''
        Check if customer has been created with the provided email only
        '''
        customer = Customer.objects.get(name="adesh")
        self.assertEqual(customer.email, "adesh.pandey10@gmail.com")

    def test_name_none(self):
        '''
        Test if we can't create customer with blank name
        '''
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                name=None, email="adesh@yopmail.com")

    def test_email_none(self):
        '''
        Test is customer can't be created with the blank email
        '''
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                name='Adesh P', email=None)

    def test_duplicate_email(self):
        '''
        Test if user email is unique
        '''
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                name="Adesh P", email="adesh.pandey10@gmail.com")


class SpecialOfferTestCase(TestCase):
    '''
    Test Special offer model
    '''

    def setUp(self):
        """
        Create a new special offer before each test cases
        """
        SpecialOffer.objects.create(name="SPO01", discount=10)

    def test_special_offer_has_discount(self):
        '''
        Check if special offer has been created with the provided discount only
        '''
        special_offer = SpecialOffer.objects.get(name="SPO01")
        self.assertEqual(special_offer.discount, 10)

class VoucherViewTestCase(TestCase):

    def test_no_vouchers(self):
        """
        If no voucher exist, an appropriate message is displayed.
        """
        response = self.client.get('/vouchers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('results'), [])

    def test_new_voucher_created(self):
        """
        Created new voucher, an appropriate message is displayed.
        """
        customer = Customer.objects.create(
            name="adesh", email="adesh.pandey10@gmail.com")
        special_offer = SpecialOffer.objects.create(name="SO#1", discount=10)

        response = self.client.post('/vouchers/', data=dict(
            customer=customer.id, special_offer=special_offer.id, expiry=datetime.now()))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('is_used'), False)

    def test_no_duplicate_voucher_created(self):
        """
        Created new voucher, an appropriate message is displayed.
        """
        customer = Customer.objects.create(
            name="adesh", email="adesh.pandey10@gmail.com")
        special_offer = SpecialOffer.objects.create(name="SO#1", discount=10)

        response = self.client.post('/vouchers/', data=dict(
            customer=customer.id, special_offer=special_offer.id, expiry=datetime.now()))

        self.assertEqual(response.status_code, 201)
        response = self.client.post('/vouchers/', data=dict(
            customer=customer.id, special_offer=special_offer.id, expiry=datetime.now()))
        self.assertEqual(response.status_code, 400)


class RedeemVoucherTestCase(TestCase):
    '''
    Test: voucher redeem process
    '''
    def test_redeem_voucher(self):
        '''
        TEST: if redeem is working as expected
        '''
        customer = Customer.objects.create(
            name="adesh", email="adesh@yopmail.com")
        special_offer = SpecialOffer.objects.create(name="SO#1", discount=10)

        res = self.client.post('/vouchers/', data=dict(
            customer=customer.id, special_offer=special_offer.id, expiry=datetime.now()))
        response = self.client.post('/redeem', data=dict(
            email="adesh@yopmail.com", code=res.data.get('code')))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data.get('discount'), special_offer.discount)

        voucher_code = VoucherCode.objects.get(code=res.data.get('code'))
        self.assertEqual(voucher_code.is_used, True)
