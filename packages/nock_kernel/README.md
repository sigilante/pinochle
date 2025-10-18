# Nock Kernel

Jupyter kernel for interactive Nock 4K evaluation.

## Installation

```bash
# Install both packages
pip install pinochle nock-kernel

# Install the kernel spec
nock-kernel-install
```

Or from source:

```bash
git clone https://github.com/sigilante/pinochle.git
cd pinochle

# Install core library
pip install ./packages/pinochle

# Install kernel
pip install ./packages/nock_kernel
nock-kernel-install
```

## Usage

The kernel is named "Nock 4K" and uses the `pinochle` library under the hood.

Start Jupyter:

```bash
jupyter notebook
```

Create a new notebook and select "Nock 4K" as the kernel.

## License

MIT License