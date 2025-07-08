from setuptools import setup, find_packages

setup(
    name='spot-sdk',
    version='0.1.0',
    description='Rackspace Spot SDK for Python',
    author='Rackspace Spot Team',
    license = "Apache-2.0",
    readme = "README.md",
    packages=find_packages(),
    install_requires=[
        'requests',
        'PyJWT',
    ],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)
