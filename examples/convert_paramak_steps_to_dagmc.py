import paramak
import gmsh2dagmc as g2d 


# stage 1 create a stp file
my_reactor = paramak.FlfSystemCodeReactor(rotation_angle=180)
my_reactor.export_stp()  # this saves several stp files including blanket.stp

# stage 2 mesh the stp file
# TODO find gmsh commands in python to perform these operations
# open gmsh gui by typing "gmsh" in the terminal
# click file open
# click 2d mesh
# click file save mesh as "example_model_from_stp.msh"

# stage 3 convert the mesh to a DAGMC h5m file
# TODO change structure to make this a one liner
data = g2d.gmshTopology('blanket.msh')
data.get_surface_data()
data.get_volume_data()
data.get_surface_topology()
data.get_vertex_data()

geom = g2d.dagmcGeom(data)
geom.transfer_geometry()
geom.export_h5m('dagmc.h5m')
