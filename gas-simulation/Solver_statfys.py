import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


#---------------------------------------------------------------------------
def Newton_rhs(r, N, R, K):
    """
    Function used to in the solver to calculate the righthandside of Newtons 
    equation.

    Parameters
    ----------
    r : array (2, N)
        Position of the particles.
    N : int
        Number of particles.
    R : float/int
        Radius of container.
    K : float
        Hardness constant of container wall.

    Returns
    -------
    rhs_x_arr, rhs_y_arr : arrays (N)
        Righthandside of Newtons equation.
    """
  
    x , y = r[0] , r[1]
    rhs_x_arr = []
    rhs_y_arr = []
    
    # Looping through all particles
    for i in range(0,N):    
        # Initializing variables
        p2p_x = 0
        p2p_y = 0
        p2w_x = 0
        p2w_y = 0
    
        # Particle-wall interaction
        R_p = np.sqrt(x[i]**2 + y[i]**2)
        if R_p > R:
            p2w_x -= K*(R_p - R)*x[i]/R_p
            p2w_y -= K*(R_p - R)*y[i]/R_p
        
        # Particle-particle interaction
        for j in range(0,N): 
            if j == i:
                continue
            else:
                dist = (x[i]-x[j])**2 + (y[i]-y[j])**2 # Using square distance
                dist = max(dist, 1e-12)
                p2p_x += (48*dist**(-6)-24*dist**(-3))* (x[i]-x[j])*dist**(-1)
                p2p_y += (48*dist**(-6)-24*dist**(-3))* (y[i]-y[j])*dist**(-1)
        
        # Calculating the resulting right-hand sides of Newtons equations
        rhs_x = p2w_x + p2p_x
        rhs_y = p2w_y + p2p_y
        
        # Storing data 
        rhs_x_arr.append(rhs_x)
        rhs_y_arr.append(rhs_y)
        
    return np.array(rhs_x_arr), np.array(rhs_y_arr)

#--------------------------------------------------------------------------

def Solve_EOM(N, R, K, dt, v0, T = 10):
    """
    Solving Newtons equations of motion using the velocity Verlet algorithm 
    for our gas in a 2D circular container.

    Parameters
    ----------
    N : int
        Number of particles.
    R : float/int
        Radius of container.
    K : float
        Hardness constant of container wall.
    dt : float
        Timestep.
    v0 : array (2, N)
        Initial velocities of the particles.
    T : int/float, optional
        Duration of simulation. The default is 10.

    Returns
    -------
    solution : array (2, T/dt, 2, N)
        Position and velocities of the particles at each timestep 
    t_arr : array (T/dt)
        Time elapsed at each timestep

    """
    
    # Initializing position of particles inside the container 
    r0 = np.zeros((2,N)) # x: r0[0], y: r0[1]   
    pi = np.pi
    
    theta_i = 2*pi/10       # Angles between particles in inner layer
    theta_y = 2*pi/(N-11)   # Angles between particles in outer layer
    
    for i in range(1,N): # First particle stays in the center  
        # Inner layer
        if i <= 10: 
            r0[0][i], r0[1][i]= R/3*np.cos(i*theta_i), R/3*np.sin(i*theta_i)
        # Outer layer
        else: 
            r0[0][i] = 2*R/3*np.cos((i-11)*theta_y)
            r0[1][i] = 2*R/3*np.sin((i-11)*theta_y)
            
    """
    # Plotting initial particle distribution     
    plt.plot(r0[0], r0[1], 'x')
    theta = np.linspace(0, 2*pi, 100)
    plt.plot(R*np.cos(theta), R*np.sin(theta))
    plt.show()  
    """
            
    # Implemmenting velocity Verlet
    solution = [[r0.copy()] , [v0.copy()]]
    r  = r0.copy()
    v  = v0.copy()
    t = 0
    t_arr = []
    t_arr.append(t)
    
    while t < T:     
        # Computing forces on all particles
        f_x, f_y = Newton_rhs(r, N, R, K)
        
        # Incrementing all possitions
       
        r[0] += v[0]*dt + .5*f_x*(dt**2)
        r[1] += v[1]*dt + .5*f_y*(dt**2)
        
        # Adding failsafe
        if not np.isfinite(r).all():
            print("Simulation unstable")
            break
         
        # Computing forces in new position
        f_xn, f_yn = Newton_rhs(r, N, R, K)
        
        # Incrementing velocity
        v[0] += .5*(f_x + f_xn)*dt
        v[1] += .5*(f_y + f_yn)*dt

        # Storing data
        solution[0].append(r.copy())
        solution[1].append(v.copy())
        
        # Incrementing time
        t += dt
        t_arr.append(t)
        
    return solution, t_arr

#----------------------------------------------------------------------------

def Energy(r,v, N, R, K):
    """
    Calculates the energy of a single state of the system.

    Parameters
    ----------
    r : array (2,N)
        Positions of all particles.
    v : array (2,N)
        Velocities of each particle.
    N : int
        Number of particles.
    R : float/int
        Radius of container.
    K : float
        Hardness constant of container wall.

    Returns
    -------
    Kinetic + Potential : float
        Total energy of the system
    Kinetic : float
        Kinetic energy of the system
    Potential : float
        Potential energy of the system

    """

    # Initializing variables
    Kinetic   = 0
    Potential = 0

    x  , y   = r[0], r[1]
    v_x, v_y = v[0], v[1]
    
    for i in range(0,N): 
        # Kinetic energy of particle
        Kinetic += .5*(v_x[i]**2 + v_y[i]**2)       
        
        # Particle-wall potential
        R_p = np.sqrt(x[i]**2 + y[i]**2)
        if R_p > R:
            Potential += .5*K*(R_p - R)**2
         
        # Particle-particle potential
        for j in range(i+1,N): 
            dist = (x[i]-x[j])**2 + (y[i]-y[j])**2 # Using square distance
            dist = max(dist,1e-12)
            Potential += 4*(dist**(-6)-dist**(-3))
    
    return Kinetic + Potential, Kinetic, Potential
                
#-----------------------------------------------------------------------------

def Relative_energy(r_arr, v_arr, N, R, K):
    
    # Calculating energy at each timestep
    en_arr = []  
    for i in range(len(r_arr)):
        E, _, _ = Energy(r_arr[i], v_arr[i], N, R, K)
        en_arr.append(E)
        
    en_arr = np.array(en_arr)
    # Calculating relative energy differance at each timestep
    dE_arr = (en_arr-en_arr[0])/en_arr[0]
    return dE_arr

#---------------------------------------------------------------------------

def Maxwell_distribution(all_v, stride = 100):
    """
    Samples velocity data form a simulated system, visualizes this by making a
    histogram and fitting a normal distribution to the data.
    Calculates the value of k_bT for the system.

    Parameters
    ----------
    all_v : array(T/dt, 2, N)
        Velocities of the paricles of the simulated system.
    stride : int, optional
        Stride for the sampeling of velocity data. The default is 100.

    Returns
    -------
    kbT : float
        k_bT for the system

    """
    
    # Sampeling data after system has setled
    i = int(0.2 * len(all_v))
    v = all_v[i::stride]          
    vx = v[:, 0, :]               

    # Removing Center of Mass drift
    vx_rel = (vx - vx.mean(axis=1, keepdims=True)).ravel()

    # Fitting normal distribution
    mu, sigma = norm.fit(vx_rel)

    # Plot histogram and fit
    x = np.linspace(vx_rel.min(), vx_rel.max(), 400)
    plt.hist(vx_rel, bins = 100, density = True, label = "Simulated data")
    plt.plot(x, norm.pdf(x, mu, sigma), label =  "Normal fit")
    plt.xlabel(r"$v_x$ ")
    plt.ylabel("Probability density")
    plt.title("Maxwell distribution of velocity")
    plt.legend(fontsize = 9)
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Calculating temperature
    kbT = np.var(vx_rel)
    return kbT

#---------------------------------------------------------------------------
def average_pressure(solution, N, R, K):
    """
    Claculating avearge preassure for a simulated system.

    Parameters
    ----------
    solution : array (2, T/dt, 2, N)
        Solution of the simulation
    N : int
        Number of particles
    R : float/int
        Radius of container
    K : float
        Hardness constant of container wall

    Returns
    -------
    P_avg : TYPE
        DESCRIPTION.

    """

    pressures = []

    start = int(0.2 * len(solution[0]))
    for r in solution[0][start:]:
       
        # Initializing variables
        F = 0
        x , y = r[0] , r[1]

        # Looping through all particles
        for i in range(0,N):    

        
            # Particle-wall interaction
            R_p = np.sqrt(x[i]**2 + y[i]**2)
            if R_p > R:
                F += K * (R_p - R)

        P = F / (2*np.pi*R)

        pressures.append(P)

    P_avg = np.mean(pressures)

    return P_avg
