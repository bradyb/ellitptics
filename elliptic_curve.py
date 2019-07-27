# Elliptic Curve Library
# Hopefully fast.
import math
import matplotlib.pyplot as plt
import numpy as np
import typing

class Point:

    def __init__(self, x: float, y: float, inf: bool=False):
        self.x = x
        self.y = y
        self.inf = inf

INFINITY = Point(0, 0, True)

class EllipticCurve:

    def __init__(self, A: float, B: float):
        if self._HasMultipleRoots(A, B):
            raise ValueError(
                'EllipticCurve(A={}, B={}) has multiple roots.'.format(A, B))
        self.A = A
        self.B = B

    def __str__(self):
        return 'EllipticCurve(A={}, B={})'.format(self.A, self.B)

    def _HasMultipleRoots(self, A: float, B: float) -> bool:
        return math.isclose(4 * A ** 3 + 27 * B ** 2, 0)

    def Draw(self):
        y, x = np.ogrid[-5:5:100j, -5:5:100j]
        plt.contour(
            x.ravel(),
            y.ravel(),
            pow(y, 2) - pow(x, 3) - x * self.A - self.B,
            [0])
        plt.grid()
        plt.show()

    def Contains(pt: Point) -> bool:
        if pt == INFINITY:
            return True
        return math.isclose(pt.y ** 2, pt.x ** 3 + self.A * pt.x + self.B)

    def AddPoints(self, pt1: Point, pt2: Point) -> Point:
        if not self.Contains(pt1) or not self.Contains(pt2):
            raise ValueError('At least one point was not on the curve.')

        if pt1 == INFINITY:
            return pt2
        elif pt2 == INFINITY:
            return pt1

        if pt1.x != pt2.x:
            slope = (pt2.y - pt1.y) / (pt2.x - pt1.x)
            x_3 = slope ** 2 - pt1.x - pt2.x
            return Point(x_3, slope * (pt1.x - x_3) - pt1.y)
        elif pt1.y != pt2.y:
            return INFINITY
        elif pt1.y != 0:
            slope = (3 * pt1.x ** 2 + self.A) / (2 * pt1.y)
            x_3 = slope ** 2 - 2 * pt1.x
            return Point(x_3, slope * (pt1.x - x_3) - pt1.y)
        else:
            return INFINITY
