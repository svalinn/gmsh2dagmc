#!/usr/env/python3
import sys
from dagmc_gmsh import gmshTopology
from dagmc import dagmcGeom

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " file.msh")
    exit(0)

data = gmshTopology(sys.argv[1])
data.get_surface_data()
data.get_volume_data()
data.get_surface_topology()
data.get_vertex_data()

geom = dagmcGeom(data)
geom.transfer_geometry()
geom.export_h5m('dagmc.h5m')
