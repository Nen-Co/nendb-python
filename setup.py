#!/usr/bin/env python3
"""
Setup script for NenDB Python Driver
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Read requirements
def read_requirements(filename):
    requirements_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.startswith("-r "):
                        # Handle recursive requirements
                        sub_file = line[3:].strip()
                        requirements.extend(read_requirements(sub_file))
                    else:
                        requirements.append(line)
            return requirements
    return []

setup(
    name="nendb",
    version="0.1.0",
    description="High-performance Python client for NenDB graph database",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Nen Team",
    author_email="team@nen.co",
    url="https://github.com/Nen-Co/nendb-python-driver",
    project_urls={
        "Bug Tracker": "https://github.com/Nen-Co/nendb-python-driver/issues",
        "Documentation": "https://docs.nen.co",
        "Source Code": "https://github.com/Nen-Co/nendb-python-driver",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt") or [],
    extras_require={
        "dev": read_requirements("requirements-dev.txt") or [],
    },
    entry_points={
        "console_scripts": [
            "nendb=nen_python_driver.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="graph,database,algorithm,bfs,dijkstra,pagerank,zig,high-performance",
)
