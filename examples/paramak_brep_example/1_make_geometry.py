import paramak

# stage 1 create a brep file
my_reactor = paramak.FlfSystemCodeReactor(rotation_angle=180)
my_reactor.export_brep('example_model_unmerged_surfaces_from_brep.brep', merge=False)

# or optionally try out a new feature that attempts to remove
# duplicate surfaces in the brep. I have not tested this fully yet
my_reactor = paramak.FlfSystemCodeReactor(rotation_angle=180)
my_reactor.export_brep('example_model_merged_surfaces_from_brep.brep', merge=True)
