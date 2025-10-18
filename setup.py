from setuptools import setup

setup(
    name='nock_kernel',
    version='1.0',
    py_modules=['nock_kernel', 'nock', 'noun'],
    install_requires=[
        'ipykernel',
        'mmh3',
        'bitstring',
    ],
)
