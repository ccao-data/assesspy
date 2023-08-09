# read the contents of your README file, remove image
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
image = '<a href="https://github.com/ccao-data/assesspy/tree/main"><img src="docs/images/logo.png" align="right" height="139"/></a>'
long_description = (this_directory / "README.md").read_text().replace(image, "")

setup(
    name="assesspy",
    version="1.0.2",
    description="General purpose Python package for measuring assessment performance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ccao-data/assesspy",
    author="CCAO",
    author_email="assessor.data@cookcountyil.gov",
    license="AGPL-3",
    packages=find_packages(),
    install_requires=["pandas", "pyarrow", "numpy", "scipy", "statsmodels"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    include_package_data=True,
    package_data={
        "": ["*.parquet"],
    },
)
