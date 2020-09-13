from distutils.core import setup
from setuptools import find_packages

setup(
    name='sieve',
    packages=find_packages(),
    package_data={'': ['*.txt']},
    version='1.0.0',
    author='Sahas Munamala',
    author_email='munamalasahas@gmail.com',
    url='https://github.com/sahasam/sieve-organizer',
    license='MIT License',
    descrption='Command line tool for organizing files',
    long_description='Organize files',
    zip_safe=False,
    entry_points={"console_scripts": ["sieve=sieve.__main__:main"]}
)
