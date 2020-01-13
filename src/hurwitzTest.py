import threading
from decimal import Decimal
from fractions import Fraction


class Equation:
    """
    an xn + a_n-1 x_n-1 + a_n-2 x_n-2 + ... + a0
    =>
    coefficients=[an,a_n-1,a_n-2,...,a_0]
    """

    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = len(coefficients)-1


def areCoefficientsPositive(coefficients):
    """
        入力された係数が全て正か調べる.
    """
    check = sum(list(map(lambda coef: coef <= 0, coefficients))) == 0
    if len(coefficients) < 2:
        check = False
    return check


def areCoefficientsSame(coefficients):
    """
        入力された係数が全て等しいか調べる.
    """
    isPositive = True if coefficients[0] > 0 else False
    if isPositive:
        return all(list(map(lambda coef: coef > 0, coefficients)))
    return all(list(map(lambda coef: coef < 0, coefficients)))


def extractTopZeros(coefficients):
    """
        最高次の係数が0だった場合,取り除く.
    """
    if len(coefficients) == 0:
        raise BaseException("given coefficients array is empty")

    """
    if len(coefficients) == 1:
        raise BaseException(
            "invalid coefficients BaseException. All of the coefficients are zeros")
    """
    # 最高次の係数が0でなかった場合,そのままreturn
    if (coefficients[0] != 0):
        return coefficients

    return extractTopZeros(coefficients[1:])


def convertToFraction(coefficients):
    """
        小数の係数を分数に変換する
    """
    return list(map(lambda each_value: Fraction(*Decimal(str(each_value)).as_integer_ratio()), coefficients))


class HurwitzBase:
    def __init__(self):
        self.coefficients = None
        self.degree: int = None
        self.P_array = None


class HurwitzStabililtyTestForRealPolymonials(HurwitzBase):
    """
        Algorithm 1.2
    """

    def __init__(self, coefficients, toFraction=True):
        super().__init__()
        self.coefficients = extractTopZeros(coefficients)
        self.degree = len(coefficients) - 1
        self.toFraction = toFraction
        if self.degree == 1:
            pass

        if toFraction:
            self.coefficients = convertToFraction(self.coefficients)

        # check args
        if not areCoefficientsSame(self.coefficients):
            print("this is not hurwitz")
        if self.coefficients[0] < 0:
            self.coefficients = list(map(lambda x: -x, self.coefficients))

    def makePolynomialQ(self, coefficients):
        Q_coefficients = []
        isEven = True

        # 数値的処理
        # mu = coefficients[0]/coefficients[1]
        if coefficients[1] == 0:
            raise BaseException("zero divide")
        mu = Fraction(coefficients[0], coefficients[1]
                      ) if self.toFraction else coefficients[0] / coefficients[1]

        # 高次の項から処理していく
        for i in range(1, len(coefficients) - 1):
            if isEven:
                Q_coefficients.append(coefficients[i])
            else:
                Q_coefficients.append(
                    coefficients[i] - mu * coefficients[i + 1])
            # 交互に処理を変える
            isEven = not isEven
        # 定数項を加える.
        Q_coefficients.append(coefficients[-1])
        if len(Q_coefficients) != len(coefficients) - 1:
            raise BaseException("invalid degreen of Q")
        return Q_coefficients

    def firstStep(self, coefficients):
        P_array = []
        P_array.append(coefficients)
        return P_array

    def secondStep(self, P_array, number: int):
        """
            *Args*
            number(int): how many times
        """
        assert number == len(P_array)-1, "mismatch number and array's length"
        if number != len(P_array)-1:
            raise BaseException("mismatch number and array's length")

        coefficients = P_array[number]
        # メソッドの終了
        if not areCoefficientsPositive(coefficients):
            return False
        return True

    def thirdStep(self, old_P_array, Q_coefficients):
        P_array = old_P_array.copy()
        P_array.append(self.makePolynomialQ(Q_coefficients))
        return P_array

    def execute(self):
        coefficients = self.coefficients

        # contain coeffients of each step.
        P_array = self.firstStep(coefficients)
        check = True
        isHurwitz = False
        count = 0

        if self.degree == 0:
            return isHurwitz

        while (True):
            check = self.secondStep(P_array, count)

            # print("coefficient positiveness", check)
            if not check:
                break

            if count >= self.degree - 2:
                isHurwitz = True
                break

            P_array = self.thirdStep(
                old_P_array=P_array, Q_coefficients=P_array[-1])
            count += 1
        self.P_array = P_array
        return isHurwitz


class Coefficients:
    def __init__(self, array_like):
        self.coefficients = array_like


class HurwitzStabililtyTestForComplexPolymonials(HurwitzBase):
    """
        Algorithm 1.3
    """

    def __init__(self, coefficients):
        self.coefficients = extractTopZeros(coefficients)
        self.degree = len(coefficients) - 1

    def firstStep(self, coefficients):
        """
        Returns
        ___
        P_array
        ____

        """
        P_array = []
        P_array.append(coefficients)
        return P_array

    def secondStep(self, P_array, number: int):
        """

        Returns
            result : boolean
        """
        if len(P_array[number]) == 1:
            return False
        assert number == len(P_array)-1, "mismatch number and array's length"
        if number != len(P_array)-1:
            raise BaseException("mismatch number and array's length")

        # Complex coefficients
        coefficients = P_array[number]

        # verify the coefficients
        """
        if len(coefficients) < 2:
            return False
            # BaseException("invalid coefficients length")
        """
        return (coefficients[0].real * coefficients[1].real +
                coefficients[0].imag * coefficients[1].imag > 0)

    def thirdStep(self, P_coefficients):
        # 最高次の係数が0でない
        if P_coefficients[0] == 0:
            # TODO
            raise BaseException("zero division")

        mu = (1/P_coefficients[0])
        # Todo
        T = list(
            map(lambda each_coefficient: each_coefficient*mu,
                P_coefficients))
        return T

    def fourthStep(self, old_P_array, Q_coefficients):
        P_array = old_P_array
        P_array.append(Q_coefficients)
        return P_array

    def makePolynomialQ(self, T_coefficients):
        # 定数項を忘れずに
        n = len(T_coefficients) - 1
        if n == 0:
            print("todo handle in makePolynomialQ")
            pass

        if T_coefficients[1] == 0:
            raise BaseException("zero divition")

        mu = 1 / T_coefficients[1].real

        # 偶数回目の処理かどうか
        isEven = True
        # 諸侯だけ最初に
        Q_coefficients = []
        # 定数項の処理だけは除く
        for i in range(1, len(T_coefficients) - 1):
            coefficient = None
            if isEven:
                coefficient = complex(
                    T_coefficients[i].real,
                    T_coefficients[i].imag - mu*T_coefficients[i + 1].imag
                )
            else:
                coefficient = complex(
                    T_coefficients[i].real - mu*T_coefficients[i + 1].real,
                    T_coefficients[i].imag
                )
            Q_coefficients.append(coefficient)
            isEven = not isEven
        # 定数項の処理
        Q_coefficients.append(T_coefficients[-1])
        return Q_coefficients

    def execute(self):
        """
        isHurwitz (boolean) : whether this polynomial is stable

        Return
        ____
        isHurwitz(boolean)
        ____
        """
        isHurwitz = False
        coefficients = self.coefficients
        P_array = self.firstStep(coefficients)
        count = 0

        while (True):
            check = self.secondStep(P_array, count)
            if not check:
                break
            if count >= self.degree-1:
                assert count == self.degree - 1, "mismatch last count"
                assert len(P_array[-1]) - \
                    1 == 1, "mismatch last array's degree"
                isHurwitz = True
                break
            # BaseException("invalid coefficients length")
            T_coefficients = self.thirdStep(P_array[-1])
            Q_coefficients = self.makePolynomialQ(T_coefficients)
            P_array = self.fourthStep(
                old_P_array=P_array, Q_coefficients=Q_coefficients
            )
            count += 1
        self.P_array = P_array
        return isHurwitz
import time

class Kharitonov:
    def __init__(self, coefficient_ranges=[]):
        """
            a x^3 + b x^2 + c x^1 +d
            -> [d,c,b,a] !!! hurwitzとはぎゃくになっていることにちゅういすべし
        """

        self.coefficient_ranges = coefficient_ranges.copy()
        # 係数の校正
        for i, each_range in enumerate(self.coefficient_ranges):
            if type(each_range) != list:
                raise BaseException("given ranges is not list")
            if len(each_range) > 2:
                raise BaseException("given range contain three")
            if len(each_range) == 1:
                self.coefficient_ranges[i].append(each_range[0])
                continue
            if each_range[0] > each_range[1]:
                raise BaseException(
                    "given range contain invalid range", each_range)

    def make_sub_polynomials(self):
        # make K1,K2
        K1, K2, K3, K4 = [], [], [], []
        degree = len(self.coefficient_ranges)-1
        for i, each_range in enumerate(reversed(self.coefficient_ranges)):
            if i % 2 == 0:
                K1.append(each_range[0])
                K2.append(each_range[0])
                K3.append(each_range[1])
                K4.append(each_range[1])
                continue
            K1.append(each_range[0])
            K2.append(each_range[1])
            K3.append(each_range[0])
            K4.append(each_range[1])
        return [K1, K2, K3, K4]

    def HurwitzTest(self, coefficients, result, index):
        if len(result) - 1 < index:
            raise BaseException("given index is over result's length")
        result[index] = HurwitzStabililtyTestForRealPolymonials(
            coefficients).execute()
        return None

    def execute(self):
        start=time.time()
        threads = []
        result = [None for i in range(4)]
        for index, K in enumerate(self.make_sub_polynomials()):
            t = threading.Thread(
                target=self.HurwitzTest,
                args=[K, result, index]
            )
            t.start()
            threads.append(t)
            #self.HurwitzTest(K, result, index)
        
        for each_thread in threads:
            each_thread.join()
        print(time.time()-start)
        print(result, "\n")
        if all(result):
            print("this polynomials family is stable (^A^)")
            return True
        print("this polynomials family is not stable (T_T)")
        return False
