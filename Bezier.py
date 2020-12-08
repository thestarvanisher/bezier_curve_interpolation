import math
import numpy as np
import matplotlib.pyplot as plt

class Bezier:
    """
    Bezier curve interpolation around points

        Attributes:
            n: The number of points around which it will be interpolated
            points: The coordinate of the points around which it will be interpolated
            curve_pts_num: The number of points on a Bezier curve between two points
    """
    n = None
    points = None
    curve_pts_num = None
    curve_pts = None
    C = None
    P = None
    A = None
    B = None

    def __init__(self, points, curve_pts_num = 30):
        """
        Initializes the class

            Parameters:
                points: The coordinate of the points around which it will be interpolated
                curve_pts_num: The number of points on a Bezier curve between two points
        """
        self.n = len(points)
        self.points = points
        self.curve_pts_num = curve_pts_num
        self.fixVariables()

    def fixVariables(self):
        """
        Fixes the type of the variables
        """
        if type(self.points) != np.ndarray:
            self.points = np.array(self.points)

    def createCoefficientMatrix(self):
        """
            Creates the coefficient matrix for the Bezier curve interpolation
        """
        C = np.zeros((self.n, self.n))

        for i in range(self.n):
            r = i + 1 if i + 1 < self.n else (i + 1) % self.n
            row = np.zeros(self.n)
            row[i], row[r] = 1, 2
            C[i] = row

        self.C = C

    def createEndPointVector(self):
        """
        Creates the column vector which contains the end points of each curve connecting two points
        """
        P = np.zeros((self.n, 2))

        for i in range(self.n):
            l = i + 1 if i + 1 < self.n else (i + 1) % self.n
            r = i + 2 if i + 2 < self.n else (i + 2) % self.n

            val = 2 * self.points[l] + self.points[r]
            P[i] = val
        
        self.P = P

    def findControlPoints(self):
        """
        Find the control points for the Bezier curve
        """
        A = np.linalg.solve(self.C, self.P)
        B = np.zeros_like(A)

        for i in range(self.n):
            l = i + 1 if i + 1 < self.n else (i + 1) % self.n
            B[i] = 2 * self.points[l] - A[l]
        
        self.A = A
        self.B = B

    def findPoints(self):
        """
        Finds the points on the smooth curve
        """
        self.createCoefficientMatrix()
        self.createEndPointVector()
        self.findControlPoints()
        
        all_pts = []

        for i in range(self.n):
            next_i = i + 1 if i + 1 < self.n else (i + 1) % self.n
            dpts = np.linspace(0, 1, self.curve_pts_num)
            for j in dpts:
                pt = np.power(1 - j, 3) * self.points[i] + 3 * j * np.power(1 - j, 2) * self.A[i] + 3 * (1 - j) * np.power(j, 2) * self.B[i] + np.power(j, 3) * self.points[next_i]
                all_pts.append(pt.tolist())

        self.curve_pts = np.array(all_pts)
    
    def getPoints(self):
        """
        Return the points on the curve. If they haven't been computed, compute them
        """
        if self.curve_pts == None:
            self.findPoints()
        
        return self.curve_pts

    def draw(self):
        """
        Draws a plot of the curve and the points
        """
        x, y = self.curve_pts[:,0], self.curve_pts[:,1]
        px, py = self.points[:,0], self.points[:,1]
        plt.plot(x, y, "b-")
        plt.plot(px, py, "ko")
        plt.axes().set_aspect('equal')
        plt.show()


    