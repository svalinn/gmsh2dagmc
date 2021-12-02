import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gmsh2dagmc",
    version="develop",
    summary="Convert gmsh files to DAGMC geometry",
    author="Andrew Davis",
    description="A Python package for converting gmsh files to DAGMC h5m files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svalinn/gmsh2dagmc",
    packages=setuptools.find_packages(),
    zip_safe=True,
    package_dir={"gmsh2dagmc": "gmsh2dagmc"},
    scripts=["gmsh2dagmc/gmsh2dagmc"],
    package_data={
        "gmsh2dagmc": [
            "requirements.txt",
            "README.md",
            "LICENSE",
        ]
    },
    classifiers=[
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    tests_require=["pytest-cov"],
    install_requires=[
        "gmsh", # testing with v4.8.4
        # "pymoab", is needed but not available on pip
        # pymoab can be install with Conda 
    ],
)