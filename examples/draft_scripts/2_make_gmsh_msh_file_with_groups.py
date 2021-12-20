
import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("my_model")

# brep files do not contain info about units
# scaling can to be applied to get geometry from mm to cm
# CAD is often in mm while neutronics codes typically use cm
# gmsh.option.setNumber("Geometry.OCCScaling", 0.1)
volumes = gmsh.model.occ.importShapes('example_model_unmerged_surfaces_from_brep.brep')
gmsh.model.occ.synchronize()

print('volumes', volumes)


ps = gmsh.model.addPhysicalGroup(2, [1])
# https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/api/gmsh.py#L711
gmsh.model.setPhysicalName(2, ps, "my surface group")

ps3 = gmsh.model.addPhysicalGroup(3, [1])
# https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/api/gmsh.py#L711
gmsh.model.setPhysicalName(3, ps3, "my vol group")

# gmsh.option.setNumber("Mesh.Algorithm", 5)
# gmsh.option.setNumber("Mesh.MeshSizeMin", 10)
# gmsh.option.setNumber("Mesh.MeshSizeMax", 10)

# VOL 2 SURF 8
# VOL 3 SURF 13
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)

entities_2d = gmsh.model.getEntities(2)
print('entities_2d', entities_2d)

entities_3d = gmsh.model.getEntities(3)
print('entities_3d', entities_3d)

entities_name = gmsh.model.getEntityName(2, 1)
print('entities_name', entities_name)

gmsh.write("example_model_merged_surfaces_from_brep.msh")
gmsh.finalize()
