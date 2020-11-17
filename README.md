# Bezier curve interpolation
## Introduction
Given `n` points, how can you draw a curve that goes around the points and is smooth?

There are infinitely many curves that could be drawn between two points in a plane. Given `n` number of points one can fit straight lines between them and a curve is drawn. In order for that curve to be smooth there must be an infinite number of points. That is practically impossible on a computer. Instead, `n` points are selected and a curve is fitted through them. When the number `n` is small, the curve looks choppy. But sometimes it is difficult to find the points on the curve, especially for a human. That's why people use computers which are able to draw a curve between two points that is smooth (it is not really smooth but on the computer screen it is, given the number of points on the curve is greater than the number of pixels). One type of a curve that a computer can draw between 2 points is a [Bezier curve](https://en.wikipedia.org/wiki/B%C3%A9zier_curve).

Sometimes, however, you might need to draw a curve that is smooth between some points. Drawing random Bezier curves between points doesn't guarantee you that the transition between points is smooth. A Bezier curve is a parametric curve which means that there is a parametric equation which could give you the points on the curve. Guaranteeing the smooth transition is achieved by solving a system of equations involving the derivative of the parametric function of that curve. The points which are interpolated describe a smooth shape, on the outline of which lie the initial points.

## How to use?
The `Bezier.py` file includes a `Bezier` class which represents a Bezier curve. In order to use it, you must first import the class.

Create the object as follows:
```python
curve = Bezier(points, curve_pts_num)
```
The arguments are as follows:
|Argument name|Default value|Description|
|-------------|-------------|-----------|
|`points`|-|A list of lists of point coordinates or a numpay array of that list. A list of point coordinates looks like `[x, y]`, where `x` is the x-axis coordinate and `y` is the y-axis coordinate of the point. For example, `[[50, 30], [100, 100]]` represents the two points `(50, 30)` and `(100, 100)`. **Important:** the points must be put in the same order as we want the curve to go through the points|
|`curve_pts_num`|30|The number of points on each of the Bezier curves. The bigger the number the smoother is the curve|

These are the available methods:
|Method|Arguments|Returns|Description|
|------|---------|-------|-----------|
|`findPoints()`|-|-|Finds the points on the smooth shape|
|`getPoints()`|-|Numpy array of the points|Returns a numpy array of the points on the outline of the smooth shape. Each sublist of that list contains point coordinates|
|`draw()`|-|-|Draws the plot of the shape. In blue is drawn the smooth outline, in black the initial points, through which the curve is interpolated|

An example of drawing a shape:
```python
points = [
    [400, 505],
    [580, 400],
    [400, 130],
    [280, 400]
]
curve = Bezier(points, 50)
curve.findPoints()
curve.draw()
```
This will find the points and draw the following plot using `matplotlib.pyplot`:
![Figure of the example plot](https://github.com/thestarvanisher/bezier_curve_interpolation/blob/main/figure.png "Example plot")

To get the points on the smooth shape outline, you can simply call
```python
curve.getPoints()
```
which will return the points as numpy array so that they can be used by another method.

## Explanation of how the interpolation works
In the code we use a cubic Bezier curve. It has the following parameterization:
![equation](https://latex.codecogs.com/svg.latex?B(t)&space;=&space;(1-t)^3P_0&space;&plus;&space;3(1-t)^2tP_1&space;&plus;&space;3(1-t)t^2P_2&space;&plus;&space;t^3P_3)

where ![equation](https://latex.codecogs.com/svg.latex?0&space;\leq&space;t&space;\leq&space;1). ![equation](https://latex.codecogs.com/svg.latex?P_0) is the first control point, also a starting point, ![equation](https://latex.codecogs.com/svg.latex?P_1,&space;P_2) - the second and third control points and ![equation](https://latex.codecogs.com/svg.latex?P_3) is the fourth control point, also an end point.

The smooth transitioning between two consecutive points is guaranteed when the first and second derivatives at the same point in both equations are respectively equal.

We obtain the first and second derivative:
<!-- $$
B'(t) = 3(1-t)^2(P_1-P_0)+6(1-t)t(P_2-P_1)+3t^2(P_3-P_2)
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=B'(t)%20%3D%203(1-t)%5E2(P_1-P_0)%2B6(1-t)t(P_2-P_1)%2B3t%5E2(P_3-P_2)%0D"></div>

## License
