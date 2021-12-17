#/usr/bin/python3
try:
    from pymoab import core, types
except ImportError as err:
    raise err('PyMoab not found, Reactor.export_h5m method not available')

import numpy as np

class dagmcGeom:
    def __init__(self, pygmsh):
        # create pymoab instance
        self.mb = core.Core()
        self.tags = dict()
        self.__make_tags()
        self.pygmsh = pygmsh
        self.moab_gmsh_verts = {}
        self.moab_gmsh_surfs = {}
        self.moab_gmsh_vols = {}
        return

    # make the all the necessary tags for
    # dagmc
    def __make_tags(self):

        SENSE_TAG_NAME = "GEOM_SENSE_2"
        SENSE_TAG_SIZE = 2
        self.tags['surf_sense'] = self.mb.tag_get_handle(
            SENSE_TAG_NAME,
            SENSE_TAG_SIZE,
            types.MB_TYPE_HANDLE,
            types.MB_TAG_SPARSE,
            create_if_missing=True)

        self.tags['category'] = self.mb.tag_get_handle(
            types.CATEGORY_TAG_NAME,
            types.CATEGORY_TAG_SIZE,
            types.MB_TYPE_OPAQUE,
            types.MB_TAG_SPARSE,
            create_if_missing=True)
        self.tags['name'] = self.mb.tag_get_handle(
            types.NAME_TAG_NAME,
            types.NAME_TAG_SIZE,
            types.MB_TYPE_OPAQUE,
            types.MB_TAG_SPARSE,
            create_if_missing=True)
        self.tags['geom_dimension'] = self.mb.tag_get_handle(
            types.GEOM_DIMENSION_TAG_NAME,
            1,
            types.MB_TYPE_INTEGER,
            types.MB_TAG_DENSE,
            create_if_missing=True)

        # Global ID is a default tag, just need the name to retrieve
        self.tags['global_id'] = self.mb.tag_get_handle(types.GLOBAL_ID_TAG_NAME)

        return

    # using pygmsh instance transfer the geometry for dagmc
    def transfer_geometry(self):
        self.make_vertices()
        self.make_surfaces()
        self.make_volumes()
        self.make_topology()

    # make the vertices
    def make_vertices(self):
        vertices = []
        for vertex in self.pygmsh.node_x.keys():
            x = self.pygmsh.node_x[vertex]
            y = self.pygmsh.node_y[vertex]
            z = self.pygmsh.node_z[vertex]
            vertices.append([x,y,z])

        # create all vertices at once
        vert_handles = self.mb.create_vertices(vertices)

        # assign vertex/handle correspondence
        for idx,vertex in enumerate(self.pygmsh.node_x.keys()):
            self.moab_gmsh_verts[vertex] = vert_handles[idx]

        return

    def make_surfaces(self):
        for surf in self.pygmsh.surface_mesh.keys():
            surface_set = self.mb.create_meshset()
            self.mb.tag_set_data(self.tags['global_id'], surface_set, surf[1])
            self.mb.tag_set_data(self.tags['category'], surface_set, "Surface")
            self.mb.tag_set_data(self.tags['geom_dimension'], surface_set, 2)

            # triangle and vertex data
            triangles = self.pygmsh.surface_mesh[surf][0][0]
            vertices = self.pygmsh.surface_mesh[surf][1][0]
            # loop over the triangles
            for idx,triangle in enumerate(triangles):
                vert1 = self.moab_gmsh_verts[vertices[idx*3]]
                vert2 = self.moab_gmsh_verts[vertices[idx*3+1]]
                vert3 = self.moab_gmsh_verts[vertices[idx*3+2]]
                verts = np.array([vert1,vert2,vert3],dtype='uint64')
                tri = self.mb.create_element(types.MBTRI, verts)
                self.mb.add_entity(surface_set,tri)

            self.moab_gmsh_surfs[surf[1]] = surface_set

    # make the surface set data
    def make_volumes(self):               
        for vol in self.pygmsh.volume_surface.keys():
            id = vol[1]
            volume_set = self.mb.create_meshset()
            self.mb.tag_set_data(self.tags['global_id'], volume_set, id)
            self.mb.tag_set_data(self.tags['category'], volume_set, "Volume")
            self.mb.tag_set_data(self.tags['geom_dimension'], volume_set, 3)
            self.moab_gmsh_vols[id] = volume_set
        return

    # set the topology
    def make_topology(self):
        # loop over the surfaces
        for surf in self.pygmsh.sense_data.keys():
            surface_id = surf[1]
            surf_handle = self.moab_gmsh_surfs[surface_id]
            # for each volume
            for vol in self.pygmsh.sense_data[surf]:
                volume_id = vol[1]
                volume_handle = self.moab_gmsh_vols[volume_id]
                self.mb.add_parent_child(volume_handle,surf_handle)

            # set the surface sense
            sense_data = self.pygmsh.sense_data[surf]
            if len(sense_data) > 1:
                senses = [self.moab_gmsh_vols[sense_data[0][1]],
                          self.moab_gmsh_vols[sense_data[1][1]]]
            else:
                senses = [self.moab_gmsh_vols[sense_data[0][1]],
                          np.uint64(0)]
                
            # set the sense tag    
            self.mb.tag_set_data(self.tags['surf_sense'], surf_handle, senses)

    def assign_metadata(self):

        # returns entities with 3 (dimenetions which are always volumes) and their ids
        dims_and_volume_ids = gmsh.model.getEntities(3)

        for dim_and_vol_id in dims_and_volume_ids:
            volume_id = dim_and_vol_id[1]
            print('get entities in volume ', volume_id' and assign to moab core')

        # not sure if this is the way to go about the setting of meta data
            # for vol in self.pygmsh.sense_data[surf]:
            #     volume_id = vol[1]
            #     volume_handle = self.moab_gmsh_vols[volume_id]
                
    def export_h5m(self,filename):
        all_sets = self.mb.get_entities_by_handle(0)
        file_set = self.mb.create_meshset()
        self.mb.add_entities(file_set, all_sets)
        self.mb.write_file(filename)
        return filename

"""    
        surface_id = 1
        volume_id = 1

        
        for item in material_dict:
            stl_filename = item['stl_filename']
            if skip_graveyard and "graveyard" in stl_filename.lower():
                continue

            surface_set = mb.create_meshset()
            volume_set = mb.create_meshset()

            # recent versions of MOAB handle this automatically
            # but best to go ahead and do it manually
            mb.tag_set_data(tags['global_id'], volume_set, volume_id)
            volume_id += 1
            mb.tag_set_data(tags['global_id'], surface_set, surface_id)
            surface_id += 1

            # set geom IDs
            mb.tag_set_data(tags['geom_dimension'], volume_set, 3)
            mb.tag_set_data(tags['geom_dimension'], surface_set, 2)

            # set category tag values
            mb.tag_set_data(tags['category'], volume_set, "Volume")
            mb.tag_set_data(tags['category'], surface_set, "Surface")

            # establish parent-child relationship
            mb.add_parent_child(volume_set, surface_set)

            # set surface sense
            sense_data = [volume_set, np.uint64(0)]
            mb.tag_set_data(tags['surf_sense'], surface_set, sense_data)

            # load the stl triangles/vertices into the surface set
            mb.load_file(stl_filename, surface_set)

            material_name = item['material']

            if skip_graveyard and "graveyard" in stl_filename.lower():
                continue

            group_set = mb.create_meshset()
            mb.tag_set_data(tags['category'], group_set, "Group")
            print("mat:{}".format(material_name))
            mb.tag_set_data(
                tags['name'],
                group_set,
                "mat:{}".format(material_name))
            mb.tag_set_data(tags['geom_dimension'], group_set, 4)

            # add the volume to this group set
            mb.add_entity(group_set, volume_set)

        all_sets = mb.get_entities_by_handle(0)

        file_set = mb.create_meshset()
        mb.add_entities(file_set, all_sets)

"""
