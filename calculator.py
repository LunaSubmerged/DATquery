import numexpr

from numpy import*

def calculate(expr):
    try:
        answer = numexpr.evaluate(expr)
        return str(answer)
    except:
        return "is not a valid expression."