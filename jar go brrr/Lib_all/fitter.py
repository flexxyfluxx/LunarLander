# fitter.py
# AP
# Version 1.1, Dec 30, 2015

from java.lang import Integer
from org.apache.commons.math3.fitting import WeightedObservedPoints, PolynomialCurveFitter
from org.apache.commons.math3.analysis.interpolation import SplineInterpolator
from org.apache.commons.math3.fitting import ACurveFitter
from org.apache.commons.math3.fitting.leastsquares import LeastSquaresBuilder
from org.apache.commons.math3.fitting.leastsquares import LeastSquaresProblem
from org.apache.commons.math3.fitting import WeightedObservedPoint
from org.apache.commons.math3.linear import DiagonalMatrix
from org.apache.commons.math3.analysis import ParametricUnivariateFunction


def toAequidistant(xrawdata, yrawdata, deltax):
    xdata = []
    ydata = []
    i = 0
    k = 0
    size = len(xrawdata) - 1
    while k < size:
        x = xrawdata[0] + deltax * i
        while k < size and not (xrawdata[k] <= x and x < xrawdata[k + 1]):
            k += 1
        if k < size:
            x1 = xrawdata[k]
            y1 = yrawdata[k]
            x2 = xrawdata[k + 1]
            y2 = yrawdata[k + 1]
            a = (y2 - y1) / (x2 - x1)
            b = y1 - a * x1
            y = a * x + b
            xdata.append(x)
            ydata.append(y)
        i += 1
    return xdata, ydata

# ------------------ Polynom fit -----------------------------------

def polynomfit(xdata, ydata, order):
    s = len(xdata)
    if order < 0:
        order = 0        
    if order > s - 1:
        order = s - 1        
    obs = WeightedObservedPoints()
    for i in range(len(xdata)):
        obs.add(xdata[i], ydata[i])
    fitter = PolynomialCurveFitter.create(order)
    coeff = list(fitter.fit(obs.toList())) 
    for i in range(s):
        ydata[i] = __poly(xdata[i], coeff)
    return coeff
                    
def __poly(x, coeff):
    y = 0
    for n in range(len(coeff)):
        y += coeff[n] * x**n
    return y


# ------------------ Spline fit ------------------------------------

def splinefit(xdata, ydata):
    from operator import itemgetter

    def func(x):
        if x < start or x > end:
            return 0
        return psf.value(x)

    s = len(xdata)
    if s < 3:
         raise ValueError("Error in splinefit. Not enough data points (minimum needed: 3)")
    start = min(xdata)
    end = max(xdata)
    data = [0] * s
    for i in range(s):
        data[i] = [xdata[i], ydata[i]]
    data.sort(key = itemgetter(0), reverse = False)
    for i in range(s):
        xdata[i] = data[i][0]
        ydata[i] = data[i][1]
    si = SplineInterpolator()
    psf = si.interpolate(xdata, ydata)
    return func

# ------------------ Function fit ----------------------------------

class MyFunc(ParametricUnivariateFunction):
    def __init__(self, func, derivatives):
        self.func = func
        self.derivatives = derivatives

    def value(self, t, parameters):
       return self.func(t, parameters)

    # Jacobian matrix of the above. In this case, this is just an array of
    # partial derivatives of the above function, with one element for each parameter.
    def gradient(self, t, parameters):
        return self.derivatives(t, parameters) 

class MyFitter(ACurveFitter):
    def __init__(self, func, derivatives, initialGuess):
        self.func = func
        self.derivatives = derivatives
        self.initialGuess = initialGuess
        
    def getProblem(self, points):
        size = len(points)
        target = [0.0] * size
        weights = [0.0] * size
        initialGuess = self.initialGuess


        i = 0
        for point in points:
            target[i] = point.getY()
            weights[i] = point.getWeight()
            i += 1

        model = ACurveFitter.TheoreticalValuesFunction(MyFunc(self.func, self.derivatives), points)
        return LeastSquaresBuilder().  \
            maxEvaluations(Integer.MAX_VALUE). \
            maxIterations(Integer.MAX_VALUE). \
            start(initialGuess).target(target). \
            weight(DiagonalMatrix(weights)). \
            model(model.getModelFunction(), model.getModelFunctionJacobian()).build()
  
def functionfit(func, derivatives, initialGuess, xdata, ydata, weights = None):
    points = []
    if weights == None:
        for i in range(len(xdata)):
            point = WeightedObservedPoint(1.0, xdata[i], ydata[i])
            points.append(point);
    else:
        for i in range(len(xdata)):
            point = WeightedObservedPoint(weights[i], xdata[i], ydata[i])
            points.append(point);
    fitter = MyFitter(func, derivatives, initialGuess)      
    coeffs = list(fitter.fit(points))
    return coeffs