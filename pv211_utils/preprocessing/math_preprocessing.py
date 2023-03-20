from sympy import sympify, latex
from sympy.printing.mathml import mathml


def exp_to_latex(exp: str):
    """ convert python expression to latex """
    return latex(sympify(exp))


def exp_to_pmathml(exp: str):
    """ convert python expression to presentation mathml """
    return mathml(sympify(exp), printer="presentation")


def exp_to_cmathml(exp: str):
    """ convert python expression to content mathml """
    return mathml(sympify(exp))
