
import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("gmsh2dagmc_model")

# brep files do not contain info about units
# scaling can to be applied to get geometry from mm to cm
# CAD is often in mm while neutronics codes typically use cm
# gmsh.option.setNumber("Geometry.OCCScaling", 0.1)
volumes = gmsh.model.occ.importShapes('example_model_unmerged_surfaces_from_brep.brep')

# this will mesh the geometry and show the result
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)
gmsh.write("example_model_unmerged_surfaces_from_brep.msh")
gmsh.finalize()
