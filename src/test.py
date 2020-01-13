
import time
from hurwitzTest2 import HurwitzStabililtyTestForComplexPolymonials, HurwitzStabililtyTestForRealPolymonials, Kharitonov
from equation import solve

"""
5x^4 + 3x^3 +1 x^2 +0 +5
=>
[5,3,1,0,5]

coeffiecient=[5,3,1,0,5]
Q_coeffiecient=[3,1,0,5]

WRONG!!
coefficients = [
    1+3j,4+2j,2+1j,4+1j
]

"""

import sys
# coefficients=[3,6,4,3,7,4,5]
#H = HurwitzStabililtyTestForRealPolymonials(coefficients)

from random import random


def makeRandomCoefficients(dim, isReal, maxRange=5, minRange=0,):
    """
    o : 0-1
    -2~2:
        (O - 0.5)*4
    -3~5:
        o*8-3
    """
    if isReal:
        return[random() * (maxRange - minRange) + minRange for w in range(dim + 1)]
    return[complex(random() * (maxRange - minRange) + minRange, random() * (maxRange - minRange) + minRange) for w in range(dim + 1)]


def randomTest(number=1000, dim=4, isReal=True):
    count = 0
    missmatch_count = 0
    time_storages = []
    while (count < number):
        each_times = []
        coefficients = makeRandomCoefficients(dim, isReal)
        if isReal:
            H = HurwitzStabililtyTestForRealPolymonials(coefficients)
        else:
            H = HurwitzStabililtyTestForComplexPolymonials(coefficients)
        t1 = time.time()
        result = H.execute()
        t2 = time.time()
        result_solve = solve(coefficients, ploting=False)
        t3 = time.time()
        time_storages.append((t2-t1, t3-t2))
        if result != result_solve:
            #print("Mismatch Result !!")
            # print(coefficients)
            # print()
            missmatch_count += 1
        count += 1
    print("{0}/{1}".format(missmatch_count, number))
    return time_storages


if __name__ == "__main__":
    if sys.argv[1] == "0":
        """
        coefficients = [
            1+3j, 4+2j, 2+1j, 4+1j
        ]
        H = HurwitzStabililtyTestForComplexPolymonials(coefficients)
        """
        # coefficients = [-1,-1]#[3, 6, 4, 3, 7, 4, 5]
        """
        
        chapter 5@
        """
        coefficients = [
            1+3j, 4+2j
        ]
        # , ,3+1j
        #H = HurwitzStabililtyTestForRealPolymonials(coefficients)
        H = HurwitzStabililtyTestForComplexPolymonials(coefficients)
        result = H.execute()
        if result:
            print("this is hurwitz")
        else:
            print("this is not hurwitz")

        result_solve = None
        if len(coefficients) != 1:
            result_solve = solve(coefficients, True)
        else:
            pass
        # print(H.P_array)

        print("\n")
        if result == result_solve:
            print("Same Result !!")
        else:
            print("Mismatch Result !!")
    elif sys.argv[1] == "1":
        values = [
            0.47874720357941836-0.19821029082774066j,
            1.1999999999999997-0.26666666666666655j
        ]
        print(values[0].real * values[1].real -
              values[0].imag * values[1].imag)
    elif sys.argv[1] == "2":
        dim=250
        times = randomTest(number=100, dim=dim, isReal=True)
        txt = ""
        for each_time in times:
            txt += ",".join(list(map(lambda x: str(x), each_time)))+"\n"
        with open("times_{0}.csv".format(str(dim)), "w", encoding="utf-8") as f:
            f.write(txt)
    elif sys.argv[1] == "3":
        # [[3, 4], [3, 7], [2, 6]] -> True
        # [[3, 4], [3, 7], [2, 6], [2, 3]] -> one False
        # [[3, 4], [3, 7], [2,7], [3, 4], [3, 5], [7, 10], [3, 6]] -> all false
        # K = Kharitonov([[3, 4], [3, 7], [2, 6]])
        K = Kharitonov([[3, 4], [3, 7], [2, 6]])
        K.execute()

"""
H = algorithm.HurwitzStabililtyTestForComplexPolymonials([
    1+1j, 2+3j, 4+6j,4+1j
])
print(H.execute())
print(H.P_array)
"""
