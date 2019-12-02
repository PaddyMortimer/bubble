# 
# .. _demo_poisson_equation:
# 
# Poisson equation
# ================
# 
# This demo is implemented in a single Python file,
# :download:`demo_poisson.py`, which contains both the variational forms
# and the solver.
# 
# This demo illustrates how to:
# 
# * Solve a linear partial differential equation
# * Create and apply Dirichlet boundary conditions
# * Define Expressions
# * Define a FunctionSpace
# * Create a SubDomain
# 
# The solution for :math:`u` in this demo will look as follows:
# 
# .. image:: poisson_u.png
#    :scale: 75 %
# 
# 
# Equation and problem definition
# -------------------------------
# 
# The Poisson equation is the canonical elliptic partial differential
# equation.  For a domain :math:`\Omega \subset \mathbb{R}^n` with
# boundary :math:`\partial \Omega = \Gamma_{D} \cup \Gamma_{N}`, the
# Poisson equation with particular boundary conditions reads:
# 
# .. math::
#    - \nabla^{2} u &= f \quad {\rm in} \ \Omega, \\
#                 u &= 0 \quad {\rm on} \ \Gamma_{D}, \\
#                 \nabla u \cdot n &= g \quad {\rm on} \ \Gamma_{N}. \\
# 
# Here, :math:`f` and :math:`g` are input data and :math:`n` denotes the
# outward directed boundary normal. The most standard variational form
# of Poisson equation reads: find :math:`u \in V` such that
# 
# .. math::
#    a(u, v) = L(v) \quad \forall \ v \in V,
# 
# where :math:`V` is a suitable function space and
# 
# .. math::
#    a(u, v) &= \int_{\Omega} \nabla u \cdot \nabla v \, {\rm d} x, \\
#    L(v)    &= \int_{\Omega} f v \, {\rm d} x
#    + \int_{\Gamma_{N}} g v \, {\rm d} s.
# 
# The expression :math:`a(u, v)` is the bilinear form and :math:`L(v)`
# is the linear form. It is assumed that all functions in :math:`V`
# satisfy the Dirichlet boundary conditions (:math:`u = 0 \ {\rm on} \
# \Gamma_{D}`).
# 
# In this demo, we shall consider the following definitions of the input
# functions, the domain, and the boundaries:
# 
# * :math:`\Omega = [0,1] \times [0,1]` (a unit square)
# * :math:`\Gamma_{D} = \{(0, y) \cup (1, y) \subset \partial \Omega\}`
#   (Dirichlet boundary)
# * :math:`\Gamma_{N} = \{(x, 0) \cup (x, 1) \subset \partial \Omega\}`
#   (Neumann boundary)
# * :math:`g = \sin(5x)` (normal derivative)
# * :math:`f = 10\exp(-((x - 0.5)^2 + (y - 0.5)^2) / 0.02)` (source
#   term)
# 
# 
# Implementation
# --------------
# 
# This description goes through the implementation (in
# :download:`demo_poisson.py`) of a solver for the above described
# Poisson equation step-by-step.
# 
# First, the :py:mod:`dolfin` module is imported: ::

from dolfin import *

# We begin by defining a mesh of the domain and a finite element
# function space :math:`V` relative to this mesh. As the unit square is
# a very standard domain, we can use a built-in mesh provided by the
# class :py:class:`UnitSquareMesh <dolfin.cpp.UnitSquareMesh>`. In order
# to create a mesh consisting of 32 x 32 squares with each square
# divided into two triangles, we do as follows ::

# Create mesh and define function space
xdmf = XDMFFile(MPI.comm_world, "2d.xdmf")
mesh = Mesh()
xdmf.read(mesh)
print('Mesh has ',mesh.num_cells(), ' cells')
V = FunctionSpace(mesh, "Lagrange", 1)

# The second argument to :py:class:`FunctionSpace
# <dolfin.functions.functionspace.FunctionSpace>` is the finite element
# family, while the third argument specifies the polynomial
# degree. Thus, in this case, our space ``V`` consists of first-order,
# continuous Lagrange finite element functions (or in order words,
# continuous piecewise linear polynomials).
# 
# Next, we want to consider the Dirichlet boundary condition. A simple
# Python function, returning a boolean, can be used to define the
# subdomain for the Dirichlet boundary condition (:math:`\Gamma_D`). The
# function should return ``True`` for those points inside the subdomain
# and ``False`` for the points outside. In our case, we want to say that
# the points :math:`(x, y)` such that :math:`x = 0` or :math:`x = 1` are
# inside on the inside of :math:`\Gamma_D`. (Note that because of
# rounding-off errors, it is often wise to instead specify :math:`x <
# \epsilon` or :math:`x > 1 - \epsilon` where :math:`\epsilon` is a
# small number (such as machine precision).) ::

# Define Dirichlet boundary (x = 0 or x = 1)
def boundary0(x):
    return x[0] == 0.0

def boundary1(x):
    return x[0] == 10.0

def bound_bubble(x, on_boundary):
    return (x[0] > 0.0 and x[0] < 10.0 and x[1] > 0.0 and x[1] < 1.0 and on_boundary)

# Now, the Dirichlet boundary condition can be created using the class
# :py:class:`DirichletBC <dolfin.fem.bcs.DirichletBC>`. A
# :py:class:`DirichletBC <dolfin.fem.bcs.DirichletBC>` takes three
# arguments: the function space the boundary condition applies to, the
# value of the boundary condition, and the part of the boundary on which
# the condition applies. In our example, the function space is ``V``,
# the value of the boundary condition (0.0) can represented using a
# :py:class:`Constant <dolfin.functions.constant.Constant>` and the
# Dirichlet boundary is defined immediately above. The definition of the
# Dirichlet boundary condition then looks as follows: ::

# Define boundary condition
p0 = Expression("0", degree=2)
bc_bubble = DirichletBC(V, p0, bound_bubble)

p1 = Constant(-50)
bc_left = DirichletBC(V, p1, boundary0)
p2 = Constant(50)
bc_right = DirichletBC(V, p2, boundary1)



# Next, we want to express the variational problem.  First, we need to
# specify the trial function :math:`u` and the test function :math:`v`,
# both living in the function space :math:`V`. We do this by defining a
# :py:class:`TrialFunction <dolfin.functions.function.TrialFunction>`
# and a :py:class:`TestFunction
# <dolfin.functions.function.TrialFunction>` on the previously defined
# :py:class:`FunctionSpace
# <dolfin.functions.functionspace.FunctionSpace>` ``V``.
# 
# Further, the source :math:`f` and the boundary normal derivative
# :math:`g` are involved in the variational forms, and hence we must
# specify these. Both :math:`f` and :math:`g` are given by simple
# mathematical formulas, and can be easily declared using the
# :py:class:`Expression <dolfin.functions.expression.Expression>` class.
# Note that the strings defining ``f`` and ``g`` use C++ syntax since,
 # for efficiency, DOLFIN will generate and compile C++ code for these
# expressions at run-time.
# 
# With these ingredients, we can write down the bilinear form ``a`` and
# the linear form ``L`` (using UFL operators). In summary, this reads ::

boundaries = MeshFunction('size_t', mesh, 1, 0)
for edge in edges(mesh):
    pt = edge.midpoint()
    if pt.x() == 0.0 or pt.x() == 10.0:
        boundaries[edge] = 1
    if edge.num_entities(2) == 1 and pt.x() > 0.0 and pt.x() < 10.0 and pt.y() > 0.1 and pt.y() < 0.9:
        boundaries[edge] = 2

ds = Measure('ds', subdomain_data=boundaries)

U = Constant((-1.0, 0.0, 0.0))
n = FacetNormal(mesh)
# Define variational problem
p = TrialFunction(V)
q = TestFunction(V)
# Body force = rho g sin(th)
rhog = Constant(10.0)
g = Expression("(x[0]-5.0)/5.0", degree=2)
k = Expression("pow(x[1], 2)*(x[1] < 0.5) + pow(1.0-x[1], 2)*(x[1]>=0.5)", degree=2)
# k = Expression("0.1 + 10*exp(-(pow(x[0] - 1.5, 2) + pow(x[1] - 0.5, 2)) / 0.02)", degree=2)
a = inner(k*grad(p), grad(q))*dx
L = k*rhog*g*q*ds(1) + dot(U, n)*q*ds(2)

# Now, we have specified the variational forms and can consider the
# solution of the variational problem. First, we need to define a
# :py:class:`Function <dolfin.functions.function.Function>` ``u`` to
# represent the solution. (Upon initialization, it is simply set to the
# zero function.) A :py:class:`Function
# <dolfin.functions.function.Function>` represents a function living in
# a finite element function space. Next, we can call the :py:func:`solve
# <dolfin.fem.solving.solve>` function with the arguments ``a == L``,
# ``u`` and ``bc`` as follows: ::

# Compute solution
p = Function(V)
p.rename('p', 'p')
solve(a == L, p, [])

# The function ``p`` will be modified during the call to solve. The
# default settings for solving a variational problem have been
# used. However, the solution process can be controlled in much more
# detail if desired.
# 
# A :py:class:`Function <dolfin.functions.function.Function>` can be
# manipulated in various ways, in particular, it can be plotted and
# saved to file. Here, we output the solution to a ``VTK`` file (using
# the suffix ``.pvd``) for later visualization and also plot it using
# the :py:func:`plot <dolfin.common.plot.plot>` command: ::

# Save solution in VTK format
file = XDMFFile(MPI.comm_world, "p.xdmf")
file.write(p)

# Project to get 'u'
V = VectorFunctionSpace(mesh, "CG", 1)
u = TrialFunction(V)
v = TestFunction(V)
a = inner(u, v)*dx

L = inner(k*(grad(p) - as_vector((rhog, 0.0, 0.0))), v)*dx

u = Function(V)
u.rename('u', 'u')
solve(a==L, u)

u_file = XDMFFile(MPI.comm_world, "u.xdmf")
u_file.write(u)
             
