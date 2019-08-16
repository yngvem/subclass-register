from setuptools import find_packages, setup

with open("README.rst") as f:
    long_description = f.read()


setup(
    name="subclass-register",
    version="1.0.1",
    license="MIT",
    description=("Automatically log all new subclasses of a specified base class."),
    long_description=long_description,
    author="Yngve Mardal Moe",
    author_email="yngve.m.moe@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
)
