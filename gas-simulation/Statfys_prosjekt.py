import numpy as np
import matplotlib.pyplot as plt
from Solver_statfys import (Solve_EOM, Energy, Relative_energy, 
                            Maxwell_distribution, average_pressure)

if __name__ == "__main__":
    
#- Initial verification of functionality -------------------------------------

    # Initializing paremeters
    N  = 10     # Number of particles
    R  = 10     # Dimensionless radius of container
    K  = 25    # Dimensionless hardness constant of container
    dt = .005   # Dimensionless time-step
    
    v0 = np.array([np.repeat(5, N), np.zeros(N)])
        
    # Solving given the paramaters above
    sol, t = Solve_EOM(N, R, K, dt, v0, 10)
    r_arr, v_arr = sol[0], sol[1]
    
    # Calculating energy at each timestep
    energy_arr = []  
    for i in range(len(t)):
        E, _, _ = Energy(r_arr[i], v_arr[i], N, R, K)
        energy_arr.append(E)
        
    # Plotting energy vs. time   
    plt.plot(t, energy_arr, color = 'seagreen')
    plt.xlabel(r"$\tilde{t}$")
    plt.ylabel(r"$\tilde{E}$", rotation = 0)
    plt.title(f"Total energy, N = {N}, dt = {dt}")
    plt.grid(True, alpha=0.3)
    plt.show()
    
#- Relative energy differance analysis ---------------------------------------    

    # Plotting relativ energy differance for different dt
    dt_arr = np.linspace(.005, .001, 5)
    print(dt_arr)
    
    for dt in dt_arr:
        sol, t = Solve_EOM(N, R, K, dt, v0, 10)
        r_arr, v_arr = sol[0], sol[1]
        dE = Relative_energy(r_arr, v_arr, N, R, K)
        plt.plot(t, dE, '--', label = f'dt = {dt}')
      
    plt.xlabel(r"$\tilde{t}$")
    plt.ylabel(r"$\frac{\tilde{E}(t) -\tilde{E}(0)}{\tilde{E}(0)}$", 
               rotation = 0, 
               labelpad = 20,
               size = 12)
    plt.title(f"Relative energy differance, N = {N}")
    plt.legend(fontsize = 8)
    plt.grid(True, alpha=0.3)
    plt.show()
    
#- Increasing number of particles ------------------------------------------

    # Initializing parameters
    R  = 15
    K  = 25     # Dimensionless hardness constant of container
    dt = .001   # Dimensionless time-step
    
    # Solving for each N
    for N in [30, 50]:       
        v0 = np.array([np.repeat(5, N), np.zeros(N)])
        sol, t = Solve_EOM(N, R, K, dt, v0, 10)
        r_arr, v_arr = sol[0], sol[1]
        
        # Calculating relative energy differance and plotting
        dE = Relative_energy(r_arr, v_arr, N, R, K)
        plt.plot(t, dE, '--', label = f'N = {N}')
        
    plt.xlabel(r"$\tilde{t}$")
    plt.ylabel(r"$\frac{\tilde{E}(t) -\tilde{E}(0)}{\tilde{E}(0)}$", 
               rotation = 0, 
               labelpad = 20,
               size = 12)
    plt.title(f"Relative energy differance, dt = {dt}")
    plt.legend(fontsize = 8)
    plt.grid(True, alpha=0.3)
    plt.show()
    
#- Plotting Maxwelldistribution and calculating T ------------------------

    # Initializing paremeters
    N  = 30     # Number of particles
    R  = 15     # Dimensionless radius of container
    K  = 25     # Dimensionless hardness constant of container
    dt = .001   # Dimensionless time-step
    
    v0 = np.array([np.repeat(2, N), np.zeros(N)])
    
    # Solving given the paramaters above
    sol, t = Solve_EOM(N, R, K, dt, v0, 100)
    r_arr, v_arr = sol[0], sol[1]
    
    # Plotting Maxwell distribution and getting K_bT 
    dE = Relative_energy(r_arr, v_arr, N, R, K)
    plt.plot(t, dE, '--', label = f'N = {N}')
    plt.show()
    kbT = Maxwell_distribution(np.array(v_arr))
    print(kbT)

   
#- Calculating and plotting the energies of the gas -------------------------
    K_arr = np.zeros(len(t))
    U_arr = np.zeros(len(t))
    E_arr = np.zeros(len(t))
    
    for i in range(len(t)):
        E, Ki, U  = Energy(r_arr[i], v_arr[i], N, R, K)
        K_arr[i] = Ki
        U_arr[i] = U
        E_arr[i] = E
        
    plt.plot(t, K_arr, label = 'Kinetic')
    plt.plot(t, U_arr, label = 'Potential')
    plt.plot(t, E_arr, label = 'Total')
    plt.xlabel(r"$\tilde{t}$")
    plt.ylabel(r"$\tilde{E}$", rotation = 0)
    plt.title(f"Energy, N = {N}, dt = {dt}")
    plt.legend(fontsize = 9)
    plt.grid(True, alpha=0.3)
    plt.show()
    
#- Verification of Ideal gas, and failure at low energy ----------------------
    
    # Initializing paremeters
    N  = 30     # Number of particles
    R  = 15     # Dimensionless radius of container
    K  = 25     # Dimensionless hardness constant of container
    dt = .001   # Dimensionless time-step
    
    # Lists for storing calculated values
    k_bT_arr = []
    p_arr    = []
    
    # Simulating for different v0
    v0_array = np.linspace(2, .005, 20) 
    for v0_x in v0_array:
        v0 = np.array([np.repeat(v0_x, N), np.zeros(N)])
        sol, t = Solve_EOM(N, R, K, dt, v0, 100)
        r_arr, v_arr = sol[0], sol[1]
        
        # Calculating k_bT and average preassure, and storing calculated values
        k_bT = Maxwell_distribution(np.array(v_arr))
        p_av = average_pressure(sol, N, R, K)
        k_bT_arr.append(k_bT)
        p_arr.append(p_av)
     
    # Calculating left- and right hand side of the ideal gass law
    A = np.pi*R**2
    ideal_gas_right = N*np.array(k_bT_arr)
    ideal_gas_left  = np.array(p_arr)*A
    
    # Plotting results
    fig, ax = plt.subplots(1,2,figsize = (12, 5))
    
    # Subplot: scatter PA vs. Nk_bT
    m = min(ideal_gas_right.min(), ideal_gas_left.min())
    M = max(ideal_gas_right.max(), ideal_gas_left.max())
    ax[0].plot([m, M], [m, M], '--', color='gray', label=r'$PA = Nk_B T$')
    ax[0].scatter(ideal_gas_right, ideal_gas_left, color='mediumpurple', )
    ax[0].set_xlabel(r'$N k_B T$')
    ax[0].set_ylabel(r'$PA$')
    ax[0].set_title('Ideal gas law')
    ax[0].grid(True, alpha=0.3)
    
    #Subplot: relative error, in percentage
    rel_err = 100*(ideal_gas_left - ideal_gas_right) / ideal_gas_right
    ax[1].plot(v0_array, rel_err, color = 'orchid')
    ax[1].set_xlabel(r'initial $v_x$')
    ax[1].set_ylabel(r'realtive error [%]')
    ax[1].set_title(r'Relative error for ideal gas')
    ax[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    