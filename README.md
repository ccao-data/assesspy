# AssessPy <a href="https://github.com/ccao-data/assesspy"><img src="https://raw.githubusercontent.com/ccao-data/assesspy/main/docs/images/logo.png" align="right" height="139"/></a>

[![package-build](https://github.com/ccao-data/assesspy/actions/workflows/python-package.yaml/badge.svg)](https://github.com/ccao-data/assesspy/actions/workflows/python-package.yaml)
[![test-coverage](https://github.com/ccao-data/assesspy/actions/workflows/test-coverage.yaml/badge.svg)](https://github.com/ccao-data/assesspy/actions/workflows/test-coverage.yaml)
[![pre-commit](https://github.com/ccao-data/assesspy/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/ccao-data/assesspy/actions/workflows/pre-commit.yaml)

Assesspy is a software package for python developed by the Cook County Assessor’s (CCAO)
Data Department. It contains many of the functions necessary to perform a standard
[sales ratio study](https://www.iaao.org/media/standards/Standard_on_Ratio_Studies.pdf).

For assessors, we believe that this package will reduce the complexity of calculating
ratio statistics and detecting sales chasing. We also hope that reporters, taxpayers,
and members of academia will find this package helpful in monitoring the performance
of local assessors and conducting research.

For detailed documentation on included functions and data, [**visit the
full reference list**](https://ccao-data.github.io/assesspy/reference.html).

For examples of specific tasks you can complete with `assesspy`
functions, see the [**vignettes page**](https://ccao-data.github.io/assesspy/vignettes.html).

## Installation

You can install the released version of `assesspy` using pip.

```python
pip install assesspy
```

Once it's installed, you can use it just like any other package. Simply
call `import assesspy` at the beginning of your script.
