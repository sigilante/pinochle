from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pinochle',
    version='1.2.0',
    author='N. E. Davis',
    author_email='neal@zorp.io',
    description='Python implementation of the Nock 4K Combinator Calculus',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sigilante/pinochle',
    packages=find_packages(),
    install_requires=[
        'mmh3',
        'bitstring',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Interpreters',
    ],
    python_requires='>=3.8',
    license='MIT',
    keywords='nock urbit jupyter kernel interpreter nockapp nockchain',
)