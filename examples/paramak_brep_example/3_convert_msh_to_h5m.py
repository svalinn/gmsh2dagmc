
import gmsh2dagmc as g2d 

# # stage 3 convert the mesh to a DAGMC h5m file
data = g2d.gmshTopology('example_model_unmerged_surfaces_from_brep.msh')
data.get_surface_data()
data.get_volume_data()
data.get_surface_topology()
data.get_vertex_data()

geom = g2d.dagmcGeom(data)
geom.transfer_geometry()
geom.assign_metadata()  # TODO this stage does not function yet
geom.export_h5m('example_model_unmerged_surfaces_from_brep.h5m')
