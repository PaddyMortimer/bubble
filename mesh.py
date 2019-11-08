import meshio

msh = meshio.read("2d.msh")
msh.prune()
print(msh)
meshio.write("2d.xdmf",msh)