import numpy as np
import matplotlib.pyplot as plt
from CR3BP_solver import CR3BP_rhs, rotating_to_inertial

def dU_tilde(x, mu):
    """
    First derivative of the effective potential U_tilde(x, 0) with respect to x
    in the Circular Restricted Three-Body Problem (CR3BP).

    Piecewise definition:
        Region I1:  x < -mu
        Region I2: -mu <= x <= 1 - mu
        Region I3:  x > 1 - mu

    Parameters
    ----------
    x : float
        Position(s) along the x-axis (non-dimensional).
    mu : float
        Mass parameter, mu = m2 / (m1 + m2).

    Returns
    -------
    dUdx : float 
        Value of dU_tilde/dx at the given x.
    """

    if x < -mu:
        return -x - (1 - mu) / (x + mu) ** 2 - mu / (x - 1 + mu) ** 2
    
    elif x <= 1 - mu:
        return -x + (1 - mu) / (x + mu) ** 2 - mu / (x - 1 + mu) ** 2
    
    else:  # x > 1 - mu
        return -x + (1 - mu) / (x + mu) ** 2 + mu / (x - 1 + mu) ** 2

def ddU_tilde(x, mu):
    """
    Second derivative of the effective potential U_tilde(x, 0) w.r.t. x 
    (CR3BP), piecewise.

    Parameters
    ----------
    x : float
        Position along the x-axis (non-dimensional).
    mu : float
        Mass parameter, mu = m2 / (m1 + m2).

    Returns
    -------
    float
        The value of dd_U_tilde/ddx at x.
    """
    if x < -mu:
        return -1 + 2*(1 - mu)/(x + mu)**3 + 2*mu/(x - 1 + mu)**3
    
    elif x <= 1 - mu:
        return -1 - 2*(1 - mu)/(x + mu)**3 + 2*mu/(x - 1 + mu)**3
    
    else:  # x > 1 - mu
        return -1 - 2*(1 - mu)/(x + mu)**3 - 2*mu/(x - 1 + mu)**3

def Newtons_method_CR3BP(x0, mu, tol = 1e-12):
    """
    Implemetation of Newtons's method for aproximation of the collinear
    Lagrange points in our Earth-Moon primary system.'

    Parameters
    ----------
    x0  : float
        Startingpoint for Newton itteration.
    tol : foalt, optional
        Sets the step tolerance. The default is 1e-12.

    Returns
    -------
    x   : float
        Position of the aproximated Lagrange point.

    """
    # First step
    x = x0
    x_new = x - dU_tilde(x, mu)/ddU_tilde(x, mu)
    
    it = 1 # Counting itterations needed to obtain a solution within tol
    
    # Running itteraton as long as the stepsize is greater than tol
    while abs(x_new -x) > tol:
        it   += 1
        x     = x_new
        x_new = x - dU_tilde(x, mu)/ddU_tilde(x, mu)
    
    
    return x_new, it

if __name__ == '__main__':
    
    mu     = 1.215e-2       # Earth–Moon mass parameter
    m1_pos = (-mu, 0.0)     # Position of the Earth
    m2_pos = (1 - mu, 0.0)  # Position of the Moon
     
    # Calcukating the different Lagrange points by starting within the different domains
    L3, it3 = Newtons_method_CR3BP(-2*mu, mu)
    L1, it1 = Newtons_method_CR3BP((1-mu)/2, mu)
    L2, it2 = Newtons_method_CR3BP(1, mu)  
    print(L1, L2, L3)
    print(it1, it2, it3)
    
    # Plotting the Lagrange points in the rotating frame of referance
    plt.scatter(*m1_pos, s=200, marker='o', label='Earth $m_1$', color = 'cadetblue')
    plt.scatter(*m2_pos, s=50, marker='o', label='Moon $m_2$', color = 'grey')
    plt.scatter(L1, 0, s=10, label = '$L_1$', color = 'indianred')
    plt.scatter(L2, 0, s=10, label = '$L_2$', color = 'brown')
    plt.scatter(L3, 0, s=10, label = '$L_3$', color = 'maroon') 
    plt.xlabel("$x'$")
    plt.ylabel("$y'$")
    plt.title("Collinear Lagrange points (CR3BP)")
    plt.legend(fontsize = 9)
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.show()
        