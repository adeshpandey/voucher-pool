from random import randint


def random_elem(arr: list):
    '''
    Select a random element from the given array
    '''
    return arr[randint(0, len(arr) - 1)]


def generate(coupon_length: int = 8) -> str:
    '''
    generate a random code of given length
    '''
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pattern = ["#" for i in range(coupon_length)]
    code = "".join([random_elem(charset) for i in pattern])
    return code
