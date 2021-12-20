

import pygmsh


# volumes = gmsh.model.occ.importShapes('example_model_merged_surfaces_from_brep.brep')

# # this will mesh the geometry and show the result
# gmsh.model.occ.synchronize()
# # gmsh.model.mesh.setSize(gmsh.model.getEntities(2), 0.1)

# # control the mesh algorithm and size
# gmsh.option.setNumber("Mesh.Algorithm", 5)
# gmsh.option.setNumber("Mesh.MeshSizeMin", 10)
# gmsh.option.setNumber("Mesh.MeshSizeMax", 10)

# gmsh.model.mesh.generate(2)
# gmsh.write("example_model_merged_surfaces_from_brep.msh")
# gmsh.finalize()

geom=pygmsh.occ.geometry.Geometry()
outDimTags= geom.import_shapes('example_model_merged_surfaces_from_brep.brep')

print(outDimTags)

# make use of add_physical(entities, label: Optional[str] = None)
# geom.add_physical(entities=[1], label='vol1')

# mesh = geom.generate_mesh()


# mesh.write('test.h5m')