
import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("my_model")


volumes = gmsh.model.occ.importShapes('example_model_merged_surfaces_from_brep.brep')

# this will mesh the geometry and show the result
gmsh.model.occ.synchronize()

# control the mesh algorithm and size
gmsh.option.setNumber("Mesh.Algorithm", 5)
gmsh.option.setNumber("Mesh.MeshSizeMin", 50)
gmsh.option.setNumber("Mesh.MeshSizeMax", 50)

gmsh.model.mesh.generate(2)
gmsh.write("example_model_merged_surfaces_from_brep.msh")
gmsh.finalize()
