from django.test import TestCase
import random

def rand_x_digit_num(x, leading_zeroes=True):
    if not leading_zeroes:
        # wrap with str() for uniform results
        return random.randint(10**(x-1), 10**x-1)  
    else:
        if x > 6000:
            return ''.join([str(random.randint(0, 9)) for i in x.range(x)])
        else:
            return '{0:0{x}d}'.format(random.randint(0, 10**x-1), x=x)