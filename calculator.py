import numexpr

from numpy import*

def calculate(expr):
    answer = numexpr.evaluate(expr)
    return answer