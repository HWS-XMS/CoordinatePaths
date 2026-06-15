from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="coordinate-paths",
    version="1.1.0",
    author="Marvin Sass",
    description="Coordinate path generation for automated scanning systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HWS-XMS/CoordinatePaths",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
    ],
)
