from setuptools import setup

setup(
    name='chalice_autodoc',
    version='0.0.1',
    description='Auto generate openapi v3 spec from a chalice app',
    url='git@github.com:whamilton/chalice_autodoc.git',
    author='William Hamilton',
    author_email='beiller@gmail.com',
    license='unlicense',
    packages=['chalice_autodoc'],
    zip_safe=True,
    install_requires=[
        'apispec==3.2.0',
        'apispec_webframeworks==0.5.2',
        'PyYAML==5.1.2',
        'chalice==1.11.0'
    ]
)
