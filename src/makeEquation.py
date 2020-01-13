import sympy

def makePolynomial(polynomial_coefs):
    x = sympy.Symbol("x")
    x_sum = 0
    for i in range(len(polynomial_coefs)):
        x_sum+=polynomial_coefs[i]*x**(len(polynomial_coefs)-1-i)
    return sympy.Poly(x_sum, x)

def getCoefs(P):
    coefs = list(map(lambda x: complex(x), P.all_coeffs()))
    print(coefs)
    return coefs

def secondStep(P_i):
    """
        P_i : sympy.Poly
    """
    coefs = getCoefs(P_i)
    print(coefs)
    return coefs[0].real*coefs[1].real+coefs[0].imag*coefs[1].imag>0

def thirdStep(P_i):
    coefs = getCoefs(P_i)
    

P = makePolynomial(polynomial_coefs=[1 + 3j, 4 + 2j, 2 + 1j, 4 + 1j])
isSatisfied = secondStep(P)
print(isSatisfied)
