from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nock_kernel',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Jupyter kernel for Nock 4K - Urbit\'s virtual machine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sigilante/pinochle',
    project_urls={
        'Bug Tracker': 'https://github.com/sigilante/pinochle/issues',
        'Documentation': 'https://github.com/sigilante/pinochle/blob/master/README.md',
        'Source Code': 'https://github.com/sigilante/pinochle',
    },
    py_modules=['nock_kernel', 'nock', 'noun'],
    install_requires=[
        'pinochle>=1.0.0',
        'ipykernel>=6.0',
        'mmh3',
        'bitstring',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Jupyter',
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