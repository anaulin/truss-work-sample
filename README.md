# Truss work sample <!-- omit in toc -->

- [System requirements](#system-requirements)
- [Setup](#setup)
- [Running `normalize_csv.py`](#running-normalizecsvpy)

# System requirements

This program uses Python 3, and has only been tested on MacOS v 10.14.3 (Mojave). To install
Python 3, see: https://www.python.org/downloads/

# Setup

1. **(optional) Set up a Python virtual environment**. This will prevent you from
   polluting your global Python installation when installing external
   dependencies.

```bash
$ python3 -m venv .venv
# You can replace '.venv' with an environment name of your choice.
```

To activate your virtual environment:

```bash
$ source .venv/bin/activate
```

This will change your environment to point at the Python installation in this
virtual environment. It will also modify your shell prompt to start with
`(.venv)`, the name of the virtual environment you're using.

Once you're done working in this virtual environment, you can deactivate it
and use your default Python installation by calling:

```bash
$ deactivate
```

2. **Install dependencies**. This program has an external dependency on the
   `dateutil` library, Python's recommended way of accessing a timezone
   database. To install it, use the `requirements.txt` file in this repository:

```bash
$ pip install -r requirements.txt
```

# Running `normalize_csv.py`

`normalize_csv.py` is an executable script that performs CSV normalization.
It expects a CSV file to be provided via `stdin`:

```bash
$ ./normalize_csv.py < sample-with-broken-utf8.csv
```

To run the tests:

```
$ python normalize_csv_test.py
```
