from setuptools import setup, find_packages

setup(
    name='belote',
    version='0.0.0-dev0',
    url='https://github.com/jisacs/belote.git',
    author='jisacs',
    description='Python3, Belote game',
    packages=find_packages(),
    install_requires=['numpy >= 1.11.1', 'pygame'],
)
