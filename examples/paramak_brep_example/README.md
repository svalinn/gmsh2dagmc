To run this example you will need some dependencies installed

create a new conda environment and install cadquery 2.1
```bash
conda create --name new_env python=3.8
conda activate new_env
conda install -c cadquery -c conda-forge cadquery=2.1
```

install pip dependencies
```bash
pip install gmsh
pip install gmsh2dagmc
pip install dagmc_h5m_file_inspector
pip install openmc_dagmc_wrapper
pip install openmc_plasma_source
```

install this repository
```bash
pip install -e git+https://github.com/shimwell/gmsh2dagmc
```

install the latest version of openmc from the development branch

