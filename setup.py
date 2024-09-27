from skbuild import setup
from setuptools import find_packages

setup(
    name='pyorbbecsdk',
    version='1.3.1',
    author='Joe Dong',
    author_email='mocun@orbbec.com',
    description='Python bindings for the Orbbec SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    cmake_install_dir='src/pyorbbecsdk',
    python_requires='>=3.6',
    install_requires=[
        'numpy<2.0',
        'opencv-python',
        'plyfile',
        'open3d',
    ],
)