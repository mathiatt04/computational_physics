import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from CR3BP_solver import CR3BP_rhs, rotating_to_inertial


def effective_potential_tilde(x, y, z, mu):
    """
    Calculates the effective potential in the CR3BP
    
    Parameters
    ----------
    x, y, z : array_like
        Position coordinates of the third body in the rotating frame. Can be scalars or NumPy arrays.
        
    mu : float
        Dimensionless mass parameter mu.

    Returns
    -------
    U_tilde : ndarray or float
        The effective potential tilde{U}(x, y, z) evaluated at the given coordinates.
    """
      
    s1 = np.sqrt((x + mu)**2 + y**2 + z**2)
    s2 = np.sqrt((x - 1 + mu)**2 + y**2 + z**2)
    return -(0.5*(x**2 + y**2)) - (1 - mu)/s1 - mu/s2 - 0.5*mu*(1 - mu)


def jacobi_constant_from_state(Y, mu):
    """
    Calculates the Jacobi integral for a given state of the CR3BP
    
    Parameters
    ----------
    Y : array_like, shape (6, N)
        State vector(s) in the rotating frame:
        [x, y, z, xi, eta, zeta], where (xi, eta, zeta) are the time derivatives of (x, y, z).
        The function accepts either a single state (6,) or multiple states (6, N) as used in solve_ivp.
        
    mu : float
        Dimensionless mass parameter mu.

    Returns
    -------
    C : ndarray or float
        Jacobi integral value(s) corresponding to each state in Y.

    """
    x, y, z, xi, eta, zeta = Y
    U_tilde = effective_potential_tilde(x, y, z, mu)
    v2 = xi**2 + eta**2 + zeta**2
    return -(v2) - 2*U_tilde



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
    Y = sol.y
    
    # Calculating the Jacobi integral and plotting the results
    C = jacobi_constant_from_state(Y, mu)
    
    plt.figure()
    plt.plot(sol.t, C, linewidth=1.2)
    plt.ticklabel_format(style='plain', useOffset=False)
    plt.xlabel(r"$\tau$")
    plt.ylabel(r"$C(\tau)$")
    plt.title("Jacobi integral vs time")
    plt.grid(True, alpha=0.3)
    plt.show()


