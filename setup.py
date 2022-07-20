from setuptools import setup, find_packages

setup(
    name="assesspy",
    version="0.1",
    description="General purpose R package for measuring assessment performance",
    url="https://gitlab.com/ccao-data-science---modeling/packages/assesspy/",
    author="CCAO",
    author_email="assessor.data@cookcountyil.gov",
    license="GPL-3",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "sklearn",
        "statsmodels"
        ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data = True,
    package_data={
        "": ["*.parquet"],
    }
    )