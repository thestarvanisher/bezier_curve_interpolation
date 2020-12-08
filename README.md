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

We obtain the first and second derivatives:
<!-- $$
B'(t) = 3(1-t)^2(P_1-P_0)+6(1-t)t(P_2-P_1)+3t^2(P_3-P_2)
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=B'(t)%20%3D%203(1-t)%5E2(P_1-P_0)%2B6(1-t)t(P_2-P_1)%2B3t%5E2(P_3-P_2)%0D"></div>

<!-- $$
B''(t) = 6(1-t)(P_2 - 2P_1 + P_0) + 6t(P_3 - 2P_2 + P_1)
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=B''(t)%20%3D%206(1-t)(P_2%20-%202P_1%20%2B%20P_0)%20%2B%206t(P_3%20-%202P_2%20%2B%20P_1)%0D"></div>

Now we let for point `i`, ![equation](https://latex.codecogs.com/svg.latex?K_i&space;=&space;P_1), ![equation](https://latex.codecogs.com/svg.latex?S_i&space;=&space;P_2). Then for example the first derivative looks like:
<!-- $$
B_i'(t) = 3(1-t)^2(K_i-P_i)+6(1-t)t(S_i-K_i)+3t^2(P_{i+1}-S_i)
$$ --> 

<div align="center"><img src="https://render.githubusercontent.com/render/math?math=B_i'(t)%20%3D%203(1-t)%5E2(K_i-P_i)%2B6(1-t)t(S_i-K_i)%2B3t%5E2(P_%7Bi%2B1%7D-S_i)%0D"></div>

In order to ensure the smooth transitioning, the following equations must be satisfied:
<!-- $$
\begin{cases}
B_i'(t=1) = B_{i+1}'(t=0) & \mbox{ for } i \in [0, n-2] \\
B_i''(t=1) = B_{i+1}''(t=0) & \mbox{ for } i \in [0, n-2] \\
B_{n-1}'(t=1) = B_0'(t=0) & \\
B_{n-1}''(t=1) = B_0''(t=0)
\end{cases}
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=%5Cbegin%7Bcases%7D%0D%0AB_i'(t%3D1)%20%3D%20B_%7Bi%2B1%7D'(t%3D0)%20%26%20%5Cmbox%7B%20for%20%7D%20i%20%5Cin%20%5B0%2C%20n-2%5D%20%5C%5C%0D%0AB_i''(t%3D1)%20%3D%20B_%7Bi%2B1%7D''(t%3D0)%20%26%20%5Cmbox%7B%20for%20%7D%20i%20%5Cin%20%5B0%2C%20n-2%5D%20%5C%5C%0D%0AB_%7Bn-1%7D'(t%3D1)%20%3D%20B_0'(t%3D0)%20%26%20%5C%5C%0D%0AB_%7Bn-1%7D''(t%3D1)%20%3D%20B_0''(t%3D0)%0D%0A%5Cend%7Bcases%7D%0D"></div>

Solving the system for `t` we get the following system of equations:
<!-- $$
\begin{cases}
K_{i+1} + S_i = 2P_{i+1} & \mbox{ for } i \in [0, n-2] \\
K_i + 2K_{i+1} = S_{i+1}+2S_i & \mbox{ for } i \in [0, n-2]\\
K_0 + S_{n-1} = 2P_0 & \\
K_{n-1} + 2K_0 = S_0 + 2S_{n-1}
\end{cases}
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=%5Cbegin%7Bcases%7D%0D%0AK_%7Bi%2B1%7D%20%2B%20S_i%20%3D%202P_%7Bi%2B1%7D%20%26%20%5Cmbox%7B%20for%20%7D%20i%20%5Cin%20%5B0%2C%20n-2%5D%20%5C%5C%0D%0AK_i%20%2B%202K_%7Bi%2B1%7D%20%3D%20S_%7Bi%2B1%7D%2B2S_i%20%26%20%5Cmbox%7B%20for%20%7D%20i%20%5Cin%20%5B0%2C%20n-2%5D%5C%5C%0D%0AK_0%20%2B%20S_%7Bn-1%7D%20%3D%202P_0%20%26%20%5C%5C%0D%0AK_%7Bn-1%7D%20%2B%202K_0%20%3D%20S_0%20%2B%202S_%7Bn-1%7D%0D%0A%5Cend%7Bcases%7D%0D"></div>

That system of equations has `2n` equations. Now, by applying little algebra to each pair of equations in the system, so the pairs are 1<sup>st</sup> and 2<sup>nd</sup>, 3<sup>rd</sup> and 4<sup>th</sup>, etc. equations, we arrive at the following system of equations:

<!-- $$
\begin{cases}
K_i + 2K_{i+1} = P_{i+2} + 2P_{i+1} \\
S_i = 2P_{i+1} - K_{i+1}
\end{cases}
$$ --> 

<div align="center"><img src="https://render.githubusercontent.com/render/math?math=%5Cbegin%7Bcases%7D%0D%0AK_i%20%2B%202K_%7Bi%2B1%7D%20%3D%20P_%7Bi%2B2%7D%20%2B%202P_%7Bi%2B1%7D%20%5C%5C%0D%0AS_i%20%3D%202P_%7Bi%2B1%7D%20-%20K_%7Bi%2B1%7D%0D%0A%5Cend%7Bcases%7D%0D"></div>


We have to be careful with the indeces as they should always be less than `n`. If an index becomes greater or equal to `n`, then the index becomes the remainder of a division with `n`. The first equation could be solved easily using a matrix of coefficients. Let `C` be the coefficient matrix, `b` be the vector of sum of the end points (right side of equation 1) and `x` be the vector of points `K` which are the second control point on each Bezier curve. Then we have to solve `Cx=b` for `x`. Matrix `C` looks like that:
<!-- $$
C_{n,n} = 
\begin{pmatrix}
1 & 2 & 0 & 0 & \cdots & 0 & 0 \\
0 & 1 & 2 & 0 & \cdots & 0 & 0 \\
0 & 0 & 1 & 2 & \cdots & 0 & 0 \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & 0 & 0 & \cdots & 1 & 2 \\
2 & 0 & 0 & 0 & \cdots & 0 & 1
\end{pmatrix}
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=C_%7Bn%2Cn%7D%20%3D%20%0D%0A%5Cbegin%7Bpmatrix%7D%0D%0A1%20%26%202%20%26%200%20%26%200%20%26%20%5Ccdots%20%26%200%20%26%200%20%5C%5C%0D%0A0%20%26%201%20%26%202%20%26%200%20%26%20%5Ccdots%20%26%200%20%26%200%20%5C%5C%0D%0A0%20%26%200%20%26%201%20%26%202%20%26%20%5Ccdots%20%26%200%20%26%200%20%5C%5C%0D%0A%5Cvdots%20%26%20%5Cvdots%20%26%20%5Cvdots%20%26%20%5Cvdots%20%26%20%5Cddots%20%26%20%5Cvdots%20%26%20%5Cvdots%20%5C%5C%0D%0A0%20%26%200%20%26%200%20%26%200%20%26%20%5Ccdots%20%26%201%20%26%202%20%5C%5C%0D%0A2%20%26%200%20%26%200%20%26%200%20%26%20%5Ccdots%20%26%200%20%26%201%0D%0A%5Cend%7Bpmatrix%7D%0D"></div>

Vector `b` looks like this:
<!-- $$
b =
\begin{bmatrix}
P_2 + 2P_1 \\
P_3 + 2P_2 \\
\vdots \\
P_0 + 2P_{n-1} \\
P_1 + 2P_0
\end{bmatrix}
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=b%20%3D%0D%0A%5Cbegin%7Bbmatrix%7D%0D%0AP_2%20%2B%202P_1%20%5C%5C%0D%0AP_3%20%2B%202P_2%20%5C%5C%0D%0A%5Cvdots%20%5C%5C%0D%0AP_0%20%2B%202P_%7Bn-1%7D%20%5C%5C%0D%0AP_1%20%2B%202P_0%0D%0A%5Cend%7Bbmatrix%7D%0D"></div>

Vector `x` looks like this:
<!-- $$
x =
\begin{bmatrix}
K_0 \\
K_1 \\
\vdots \\
K_{n-1}
\end{bmatrix}
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=x%20%3D%0D%0A%5Cbegin%7Bbmatrix%7D%0D%0AK_0%20%5C%5C%0D%0AK_1%20%5C%5C%0D%0A%5Cvdots%20%5C%5C%0D%0AK_%7Bn-1%7D%0D%0A%5Cend%7Bbmatrix%7D%0D"></div>

Then we have to solve the following equation for `x`:
<!-- $$
Ax = b \Rightarrow x = A^{-1}b
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=Ax%20%3D%20b%20%5CRightarrow%20x%20%3D%20A%5E%7B-1%7Db%0D"></div>

Now we can easily find the third control point for each Bezier curve by solving equation 2 in the system. Then we have obtained all the control points. Then for each of the `n` curves we get a set of `m ` points (this corresponds to `curve_pts_num`) such that:
<!-- $$
\gamma_j = \frac{j}{m},\; j \in [0, m]
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=%5Cgamma_j%20%3D%20%5Cfrac%7Bj%7D%7Bm%7D%2C%5C%3B%20j%20%5Cin%20%5B0%2C%20m%5D%0D"></div>

Then each point `G` on on the closed path for the `n` Bezier curves could be found using these equations:
<!-- $$
\begin{cases}
G_i(t = \gamma_j) = (1-t)^3P_i + 3t(1-t)^2K_i+3t^2(1-t)S_i+t^3P_{i+1},\; i \in [0, n-2],\; j \in [0, m] \\
G_{n-1}(t = \gamma_j) = (1-t)^3P_{n-1} + 3t(1-t)^2K_i+3t^2(1-t)S_i+t^3P_0,\; j \in [0, m]
\end{cases}
$$ --> 

<div><img src="https://render.githubusercontent.com/render/math?math=%5Cbegin%7Bcases%7D%0D%0AG_i(t%20%3D%20%5Cgamma_j)%20%3D%20(1-t)%5E3P_i%20%2B%203t(1-t)%5E2K_i%2B3t%5E2(1-t)S_i%2Bt%5E3P_%7Bi%2B1%7D%2C%5C%3B%20i%20%5Cin%20%5B0%2C%20n-2%5D%2C%5C%3B%20j%20%5Cin%20%5B0%2C%20m%5D%20%5C%5C%0D%0AG_%7Bn-1%7D(t%20%3D%20%5Cgamma_j)%20%3D%20(1-t)%5E3P_%7Bn-1%7D%20%2B%203t(1-t)%5E2K_i%2B3t%5E2(1-t)S_i%2Bt%5E3P_0%2C%5C%3B%20j%20%5Cin%20%5B0%2C%20m%5D%0D%0A%5Cend%7Bcases%7D%0D"></div>

## License
