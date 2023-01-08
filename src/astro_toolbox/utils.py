def negative_support_pow(value, exponent):
    if (value < 0): 
        return -((-value)**(exponent))
    else: 
        return value**(exponent)