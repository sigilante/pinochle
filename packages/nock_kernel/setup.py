from setuptools import setup

setup(
    name='nock-kernel',
    version='1.2.1',
    author='N. E. Davis',
    author_email='neal@zorp.io',
    description='Jupyter kernel for interactive Nock evaluation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sigilante/pinochle',
    packages=['nock_kernel'],
    package_data={
        'nock_kernel': ['kernelspec/kernel.json'],
    },
    include_package_data=True,
    install_requires=[
        'pinochle>=1.2.1',
        'ipykernel>=6.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    keywords='nock urbit jupyter kernel',
)