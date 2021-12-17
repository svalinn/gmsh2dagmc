import paramak
import gmsh2dagmc as g2d 
import gmsh

# stage 1 create a brep file
my_reactor = paramak.FlfSystemCodeReactor(rotation_angle=180)
my_reactor.export_brep('example_model_merged_surfaces_from_brep.brep', merge=True)

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("gmsh2dagmc_model")

# brep files do not contain info about units
# scaling can to be applied to get geometry from mm to cm
# CAD is often in mm while neutronics codes typically use cm
# gmsh.option.setNumber("Geometry.OCCScaling", 0.1)
volumes = gmsh.model.occ.importShapes('example_model_merged_surfaces_from_brep.brep')

# this will mesh the geometry and show the result
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)
gmsh.write("example_model_merged_surfaces_from_brep.msh")
gmsh.finalize()

# stage 3 convert the mesh to a DAGMC h5m file
data = g2d.gmshTopology('example_model_merged_surfaces_from_brep.msh')
data.get_surface_data()
data.get_volume_data()
data.get_surface_topology()
data.get_vertex_data()

geom = g2d.dagmcGeom(data)
geom.transfer_geometry()
geom.assign_metadata()  # TODO this stage does not function yet
geom.export_h5m('example_model_unmerged_surfaces_from_brep.h5m')

# to inspect the resulting h5m file 
# pip install inspect-dagmc-h5m-file shows that there are no tagged materials or volume ids
# inspect-dagmc-h5m-file -i example_model_unmerged_surfaces_from_brep.h5m -v -m
