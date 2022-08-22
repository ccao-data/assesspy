from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="assesspy",
    version="0.1",
    description="General purpose Python package for measuring assessment performance",
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