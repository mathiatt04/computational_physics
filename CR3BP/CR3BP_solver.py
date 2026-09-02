import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def CR3BP_rhs(tau, X_arr):
    """
    Computes the right-hand side of the non-dimensional CR3BP equations.

    Parameters
    ----------------
    tau     : float
            Dimensionless time variable (tau = wt).
    X_arr   : array_like, shape (6,)
            State vector [x, y, z, xi, eta, zeta], where:
                x, y, z : float
                    Position components of the small body in the rotating frame.
                xi, eta, zeta : float
                    Velocity components with respect to tau.

    Returns
    ---------------
    dYdtau  : ndarray, shape (6,)
            Time derivative of the state vector:
            [dx/dtau, dy/dtau, dz/dtau, d^2x/dtau^2, d^2y/dtau^2, d^2z/dtau^2].

    Notes
    ---------------
    The system models the Circular Restricted Three-Body Problem (CR3BP)
    in a rotating reference frame, using the standard non-dimensionalized
    formulation with characteristic distance 'a = 1' and angular velocity 'w = 1'.
    """
    mu     = 1.215e-2
    x, y, z, xi, eta, zeta = X_arr
    
    # Distance to the two primaries 
    s1_3 = ((x + mu)**2 + y**2 + z**2)**(3/2)
    s2_3 = ((x - 1 + mu)**2 + y**2 + z**2)**(3/2)
    
    
    # Calculation of the second-derivatives
    xdd = 2 * eta + x - (1 - mu) * (x + mu) / s1_3 - mu * (x - 1 + mu) / s2_3
    ydd = -2 * xi + y - (1 - mu) * y / s1_3 - mu * y / s2_3
    zdd = - (1 - mu) * z / s1_3 - mu * z / s2_3
    
    
    return np.array([xi, eta, zeta, xdd, ydd, zdd])


def rotating_to_inertial(t, xR, yR, zR, omega = 1.0, is_tau = True):
    """
    Parameters
    ----------------------
    t : array_like
        Time samples. If `is_tau` is True, this is tau = omega*t (non-dimensional time).
        Otherwise it is the physical time t (seconds) and `omega` is used.
        
    xR, yR, zR : array_like
        Rotating-frame coordinates at each time sample. Must be broadcastable to the shape of `t`.
        
    omega : float, optional
        Angular rate omega of the rotating frame. Default 1.0.
        
    is_tau : bool, optional
        If True, interpret `t` as tau so the rotation angle is theta = tau.
        If False, interpret `t` as physical time and use theta = omega*t.

    Returns
    -----------------------
    xI, yI, zI : ndarray
        Inertial-frame coordinates at the same time samples.

    """
    
    # Ensures data is stored in numpy arrays 
    t = np.asarray(t)
    xR, yR, zR = np.asarray(xR), np.asarray(yR), np.asarray(zR)
    
    # Sets the rotation angle theta
    theta = t if is_tau else omega * t
    cos, sin = np.cos(theta), np.sin(theta)
    
    # Implementing the effect of the rotation matrix
    xI = cos * xR - sin * yR
    yI = sin * xR + cos * yR
    zI = zR
    
    return xI, yI, zI
    



if __name__ == '__main__':
    
    # Parameters
    mu     = 1.215e-2        # Earth–Moon mass parameter (example)
    t_span = (0.0, 25.0)     # dimensionless time interval tau \in [0, T]
    t_array = np.linspace(t_span[0], t_span[1], 5000)
    
    r_phys = 6600       # Radius of our LOE [km]
    a      = 3.850e5    # Given a-value for the earth and moon [km]
    r_nd   = r_phys / a # Non-dimensionalized radius for LOE
    
    
    # Example Initial conditions (planar example: z = zeta = 0) 
    # Starting in low earth orbit, placing the satelite along the x' axis.
    x0, y0, z0 = -mu + r_nd, 0.0, 0.0
    xi0, eta0, zeta0 = 0.0, 10.7, 0.0
    Y0 = np.array([x0, y0, z0, xi0, eta0, zeta0])
    
    
    # Integrate with DOP853 
    sol = solve_ivp(
        CR3BP_rhs, t_span, Y0, t_eval=t_array,
        method="DOP853", rtol=1e-10, atol=1e-12)
      
    if not sol.success:
        raise RuntimeError(sol.message)
        
        
    # Storing solutions for the planar motion
    x = sol.y[0]
    y = sol.y[1]
    z = sol.y[2]
    
    # Positions of primaries in this normalization
    m1_pos = (-mu, 0.0)
    m2_pos = (1 - mu, 0.0)
    
    # Plotting planar motion
    plt.figure(figsize=(6,6))
    plt.plot(x, y, linestyle = '--', color = 'maroon')
    plt.scatter(*m1_pos, s=80, marker='o', label='Earth $m_1$', color = 'cadetblue')
    plt.scatter(*m2_pos, s=40, marker='o', label='Moon $m_2$', color = 'grey')
    plt.axis('equal')
    plt.xlabel("$x'$")
    plt.ylabel("$y'$")
    plt.title("Planar trajectory in rotating frame (CR3BP)")
    plt.legend(fontsize = 9)
    plt.grid(True, alpha=0.3)
    plt.show()
    
    
    # Applying the rotation matrix to our planar motion example
    xI, yI, zI = rotating_to_inertial(t_array, x, y, z)
    
    # Calculating the orbits of the primaries 
    x1_orbit = -mu * np.cos(t_array)
    y1_orbit = -mu * np.sin(t_array)
    x2_orbit = (1 - mu) * np.cos(t_array)
    y2_orbit = (1 - mu) * np.sin(t_array)
    
    plt.figure(figsize=(6,6))
    plt.plot(x1_orbit, y1_orbit, label='Earth $m_1$', color = 'cadetblue', linewidth = 3)
    plt.plot(x2_orbit, y2_orbit, label='Moon $m_2$', color = 'grey')
    plt.plot(xI, yI, linestyle = '--', color = 'maroon')
    plt.axis('equal')
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("Planar trajectory in inertal frame (CR3BP)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

