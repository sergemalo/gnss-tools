from setuptools import find_packages, setup

setup(
    name='nmealib',
    packages=find_packages(include=['nmealib']),
    version='0.1.0',
    description='SM NMEA Lib',
    author='Serge Malo',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
