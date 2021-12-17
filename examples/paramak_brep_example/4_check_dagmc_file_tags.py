import dagmc_h5m_file_inspector as di

tags = di.get_volumes_and_materials_from_h5m("example_model_unmerged_surfaces_from_brep.h5m")

print(tags)

print('no volume tags and no material tags are found')