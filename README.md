# Computational physics projects

Two numerical projects in Python, written for TMA4320 *Introduction to Scientific Computation*
at NTNU, spring 2025. Both solve a physics problem end to end: derive the scheme, implement it,
verify it converges, then run it and interpret what comes out.

| Project | Problem | Core methods |
|---|---|---|
| [**Josephson junctions via the Usadel equation**](usadel-josephson/) | Superconducting proximity effect in an S–N–S junction | Adaptive Runge–Kutta, shooting method, boundary value problems, parallelisation |
| [**Cahn–Hilliard phase separation**](cahn-hilliard/) | Spinodal decomposition in a binary mixture | Fourier spectral methods, IMEX time integration, convergence analysis |

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

Both projects were written in pairs, as the course required. **[Partner's full name]**
co-authored both. The written reports were prepared jointly in LaTeX.

My main individual contributions were **[fill in honestly — e.g. the analytical proof
that the current integrand is conserved (report 2, task 2m), the stability-boundary
derivation in report 3 task 3c, the Riccati packing/unpacking layer and its tests]**.

## Note on course material

Published with the permission of the course coordinator. The exercise sheets themselves
are not reproduced here; only our own solutions, code and write-ups.

## Licence

Code is released under the MIT licence (see `LICENSE`). The written reports are
© the authors and are included for reference rather than reuse.
