import paramak

# stage 1 create a brep file
my_reactor = paramak.FlfSystemCodeReactor(rotation_angle=180)
my_reactor.export_brep('example_model_merged_surfaces_from_brep.brep')

