# 26-Sep-2019 05:31:31 PM

## Splines

**Constraints**:  

- Interpolate $n$ points $x_k$ using cubics

$$
S(x) = \begin{cases}
S_1(x) \text{ for } x_1 \leq x \leq x_2\\
S_2(x) \text{ for } x_2 \leq x \leq x_3\\
\vdots \\
S_{n-1}(x) \text{ for } x_{n-1} \leq x \leq x_n
\end{cases}
$$

of the form

$$S_k(x) = a_k (x-x_k)^3 + b_k (x-x_k)^2 + c_k (x-x_k) + y_k$$

so that $S_k(x_k) = y_k$. There are $4 (n-1)$ degrees of freedom.

- $S \in C^2$ is twice differentiable -- so we must have $S^{(k)}_{j-1}(x_j) = S^{(k)}_j(x_j)$ for $k=0,1,2$.

  - $S_k$

    - $S_1(x_2) = y_2$

      $$a_1 h^3 + b_1 h^2 + c_1 h + y_1 = y_2$$

    - $\vdots$

    - $S_{n-1}(x_n) = y_n$, which implies for

    $$a_k h^3 + b_k h^2 + c_k h + y_{k} = y_{k+1}$$

  - $S_k'$

    - $3 a_k h^2 + 2 b_k h + c_k = c_{k+1}$

  - $S_k''$

    - $6 a_k h + 2 b_k  = 2 b_{k+1}$

This leaves us with $4(n-1) - 2$ equations — $2$ fewer than the number of unknowns. The remaining two are given by boundary conditions on $S^{(2)}$ (at the end points). This is a freedom, because it is not fixed by the curvature of a section on just one side of the point.

- We have $b_i = S''(x_i)/2$, which implies $a_i = \frac{S''(x_{i+1}) - S''(x_i)}{6h}$.
- We have $c_i = y_{i+1} - y_i - \frac{S''(x_{i+1}) - S''(x_i)}{6} h - S''(x_{i}) h^2/2$

## Theorem: Cubic Spline Interpolation

Given $n$ points $(x_i, y_i)$ with $x_{i+1} - x_i = h$, the cubic spline

$$
S(x) = \begin{cases}
S_1(x) \text{ for } x_1 \leq x \leq x_2\\
S_2(x) \text{ for } x_2 \leq x \leq x_3\\
\vdots \\
S_{n-1}(x) \text{ for } x_{n-1} \leq x \leq x_n
\end{cases}
$$

of the form

$$S_k(x) = a_k h^3 + b_k h^2 + c_k h + d_k$$

that interpolate the oints have coefficients given by

$$a_i = \frac{M_{i+1} - M_i}{6h}$$

$$b_i = M_i/2$$

$$c_i = \frac{y_{i+1}-y_i}{h} - \frac{M_{i+1} + 2 M_i}{6}h$$

$$d_i = y_i$$

where $M_i = S''(x_i)$.

---

In terms of $M_i$, $S'$ continuous implies

$$M_i + 4 M_{i+1} + M_{i+2} = \frac{6}{h^2} (y_{i+2} - 2 y_{i+1} + y_i)$$

for $i \in \{1, \ldots, n-2\}$.

We can express this recurrence relation in matrix form as

$$\mathbf{A} \mathbf{m} = \frac{6}{h^2} \mathbf{\bar y}$$

where $\mathbf{m} = \begin{bmatrix} M_1 \\ \vdots \\ M_{n} \end{bmatrix}$ and $\mathbf{\bar y} = \begin{bmatrix} y_1 - 2 y_2 + y_3 \\ \vdots \\ y_{n-2} - 2 y_{n-1} + y_n\end{bmatrix}$. The matrix $\mathbf{A}$ takes the form

$$\mathbf{A} = \begin{bmatrix}
  1 & 4 & 1 & 0 & \cdots & 0 & 0 & 0 \\
  0 & 1  & 4 & 1 & \cdots & 0 & 0 & 0 \\
  0 & 0 & 1 & 4 & \cdots & 0 & 0 & 0\\
  \vdots & \vdots & \ddots & \ddots & \ddots & \vdots & \vdots & \vdots \\
  0 & 0 & 0 & \cdots & 1 & 4 & 1 & 0\\
  0 & 0 & 0 & \cdots & 0 & 1 & 4 & 1
\end{bmatrix}.$$

---

#### Natural Spline $M_1 = M_n = 0$

#### Parabolic Runout Spline $a_1 = a_n = 0 \implies M_1 = M_2 \text { and } M_{n-1} = M_n$

The spine is parabolic on the first and last intervals.

#### Cubic Runout Spline

The first and last two intervals are each a single cubic.

$$a_1 = a_2 \text{ and } a_{n-1} = a_{n-2}$$
implies
$$M_1 = 2M_2 - M_3 \text { and } M_{n-1} = 2M_{n-2} - M_{n-3}$$
