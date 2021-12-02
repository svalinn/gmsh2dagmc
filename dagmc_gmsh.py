import gmsh
import sys

class gmshTopology:
    def __init__(self,filename):
        gmsh.initialize()
        self.load_file(filename)
        print("Model name: " + gmsh.model.getCurrent())
        self.entities = gmsh.model.getEntities()
        self.volume_surface = {}
        self.surface_mesh = {}
        self.sense_data = {}
        self.node_x = {}
        self.node_y = {}
        self.node_z = {}
        
    # load the named file
    def load_file(self,filename):
        gmsh.open(filename)

    # get all the vertex data
    def get_vertex_data(self):
        nodeTags, nodeCoords, _ = gmsh.model.mesh.getNodes()
        self.node_x = dict(zip(nodeTags, nodeCoords[0::3]))
        self.node_y = dict(zip(nodeTags, nodeCoords[1::3]))
        self.node_z = dict(zip(nodeTags, nodeCoords[2::3]))
        return
        
    # get the surface mesh data
    def get_surface_data(self):
        for e in self.entities:
            if gmsh.model.getType(e[0], e[1]) != "Discrete surface":
                continue
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(e[0], e[1])
            
            self.surface_mesh[e] = (elemTags,elemNodeTags)
#            print(elemTypes,elemTags,elemNodeTags)
        return
    
    # get the volume surface data
    def get_volume_data(self):
        for e in self.entities:
            if gmsh.model.getType(e[0], e[1]) != "Discrete volume":
                continue
            boundary = gmsh.model.getBoundary([e])
            self.volume_surface[e] = boundary
        return

    # check to make sure surface is shared by
    # no more than 2 volumes
    def check_surface_topology(self):
        for surf in self.sense_data.keys():
            if len(self.sense_data[surf]) > 2:
                print ("surface is shared by more than 2 volumes")
                return False
                   
        return True
    
    # generate the surface topology - surface senses
    def get_surface_topology(self):
        for vol in self.volume_surface.keys():
            for surf in self.volume_surface[vol]:
                if surf not in self.sense_data.keys():
                    self.sense_data[surf] = [vol]
                else:
                    self.sense_data[surf].append(vol)
        if not self.check_surface_topology():
            sys.exit(0)
        return 
