# voucher-pool

# A voucher generation/redeem application which demonstrates following things:

1. How to generate random 8 digit coupon codes with the combination of alphanumeric characters which constitutes 2^63 combinations. 
2. How to build and test django app using django testing framework
3. How to setup CI/CD with github actions

## What are the features:
1. APIs to manage the customers/offers/vouchers
2. Admin backend to handle the same.
3. pycodestyle to check the pep8 code styles
4. Local setup using docker compose
5. CI pipeline pushing to the docker hub
6. CD pushing to heroku

## Endpoints

'''
{
    "customers": "http://localhost:8000/customers/",
    "offers": "http://localhost:8000/offers/",
    "vouchers": "http://localhost:8000/vouchers/"
    "redeem": "http://localhost:8000/redeem"
}
'''

## TODO
1. Improve the views/serializers
2. Apply some cryptographic algorightm to make the coupons more secure and standard
3. Introducing .env for the docker-compose env variables
4. Better migration management.