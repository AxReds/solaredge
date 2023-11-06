import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="solaredge_exporter",
    version="0.0.1",
    description="A package for exporting your data from the SolarEdge monitoring dashboard through SolarEdge APIs",
    package_dir={"": "solaredge_exporter"},
    packages=setuptools.find_packages(where="solaredge_exporter"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AxReds/solaredge",
    author="AxReds",
    author_email="alessior@live.com",
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    install_requires=[
        # List your package's dependencies here
        "requests"
    ],
    #entry_points={
    #    # Define your package's entry points here
    #}
    python_requires='>=3.6',
)
