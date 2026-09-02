import numpy as np
import matplotlib.pyplot as plt
from CR3BP_solver import CR3BP_rhs, rotating_to_inertial
from scipy.integrate import solve_ivp


# Parameters
mu     = 1.215e-2        # Earth–Moon mass parameter (example)
t_span = (0.0, 25.0)     # dimensionless time interval tau \in [0, T]
t_array = np.linspace(t_span[0], t_span[1], 5000)

L1 = 0.8369180073169304


x0, y0, z0 = L1, 0, 0
xi0, eta0, zeta0 = 0, 0, 0
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

# Position of the moon
m2_pos = (1 - mu, 0.0)

# Plotting planar motion in rotating frame
plt.figure(figsize=(6,6))
plt.plot(x, y, linestyle = '--', color = 'maroon')
plt.scatter(*m2_pos, s=60, marker='o', label='Moon $m_2$', color = 'grey')
plt.scatter(L1, 0, s=30, label = '$L_1$', color = 'indianred')
plt.axis('equal')
plt.xlabel("$x'$")
plt.ylabel("$y'$")
plt.title("Orbit starting in $L_1$ (Rotating frame)")
plt.legend(fontsize = 9)
plt.grid(True, alpha=0.3)
plt.show()

# Converitng orbit to inertial frame
xI, yI, zI = rotating_to_inertial(t_array, x, y, z)

# Calculating the orbit of the moon
x2_orbit = (1 - mu) * np.cos(t_array)
y2_orbit = (1 - mu) * np.sin(t_array)

plt.figure(figsize=(6,6))
plt.plot(x2_orbit, y2_orbit, label='Moon $m_2$', color = 'grey', linewidth=2)
plt.plot(xI, yI, linestyle = '--', color = 'maroon')
plt.axis('equal')
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.title("Orbit starting in $L_1$ (Inertial frame)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


