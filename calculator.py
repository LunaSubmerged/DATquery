import numexpr


def calculate(expr):
    try:
        answer = numexpr.evaluate(expr)
        return str(answer)
    except Exception:
        return "is not a valid expression."
