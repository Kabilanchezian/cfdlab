"""
This demo program solves Poisson's equation

    (u^2/2)_x - u_xx = f(x)

on the unit interval with source f given by

    f(x) = 9*pi^2*sin(3*pi*x[0])

and boundary conditions given by

    u(0) = u(1) = 0
"""

from dolfin import *

# Read mesh
mesh = Mesh("mesh.xml")

# FE function space
V    = FunctionSpace(mesh, "CG", 1)

# Sub domain for Dirichlet boundary condition
def DirichletBoundary(x):
     return x[0] < DOLFIN_EPS or x[0] > 1.0 - DOLFIN_EPS

# Define variational problem
f = Expression("10.0*x[0]*(1.0-x[0])*sin(x[0])")
g = grad(f)

u  = Function(V)
du = TrialFunction(V)
v  = TestFunction(V)

F = (-0.5*u**2*v.dx(0) + inner(grad(u), grad(v)))*dx - f*v*dx
dF= derivative(F, u, du)

# Define boundary condition
u0 = Constant(0.0)
bc = DirichletBC(V, u0, DirichletBoundary)

# Solve PDE
primal = VariationalProblem(F, dF, bc)
primal.solve(u)

# Save solution to file
File("primal.pvd") << u
File("primal.xml") << u.vector()
