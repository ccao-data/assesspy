from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="assesspy",
    version="0.1.3",
    description="General purpose Python package for measuring assessment performance",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.com/ccao-data-science---modeling/packages/assesspy/",
    author="CCAO",
    author_email="assessor.data@cookcountyil.gov",
    license="GPL-3",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "pyarrow",
        "numpy",
        "scipy",
        "sklearn",
        "statsmodels"
        ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    include_package_data = True,
    package_data={
        "": ["*.parquet"],
    }
    )