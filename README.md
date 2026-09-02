# Computational physics projects

A number of numerical projects in Python, written as part of coursework at NTNU. Each one solves a physics problem end to end by deriving the scheme, implementig it,
verifying it converges, then run it and interpret what comes out.

| Project | Problem | Core methods |
|---|---|---|
| [**Josephson junctions via the Usadel equation**](usadel-josephson/) | Superconducting proximity effect in an S-N-S junction | Adaptive Runge-Kutta, shooting method, boundary value problems, parallelisation |
| [**Cahn-Hilliard phase separation**](cahn-hilliard/) | Spinodal decomposition in a binary mixture | Fourier spectral methods, IMEX time integration, convergence analysis |
| [**Circular restricted three-body problem**](CR3BP/)  | Lagrange points and translunar trajectories in the Earth-Moon system | High-order Runge-Kutta (DOP853), Newton's method, conserved-quantity verification

Each folder has its own README, the notebook, and the written report.

## Running the code

```bash
pip install -r requirements.txt
jupyter lab
```

Both notebooks run top to bottom on a laptop. The Usadel notebook uses
`ProcessPoolExecutor`, so run it as a script or in Jupyter rather than in an
environment without proper multiprocessing support.

## Authorship

The Josephson-junction and Cahn-Hilliard projects were written in groups of three, per course requirements. Mina Vikdal Cook and Trond Christian Jensen Haug co-authored both. The written reports were prepared jointly in LaTeX.

My main individual contributions were most of the theoretical derivations in both projects, as well as implementing the IMEX method, improving runtime by utilizing multiple processor cores, and writing docstrings for most functions.

## Note on course material

Published with the permission of the course coordinator. The exercise sheets themselves
are not reproduced here; only our own solutions, code and write-ups.

## Licence

Code is released under the MIT licence (see `LICENSE`). The written reports are
© the authors and are included for reference rather than reuse.
