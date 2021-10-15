import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="foxrestapiclient",
    version="0.1.5",
    description="Connect to F&F Fox devices via RestAPI.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="F&F Filipowski Sp. j.",
    author_email="t.waclawiak@fif.com.pl",
    license="MIT",
    url = "https://github.com/fandf92/foxrestapiclient",
    packages=find_packages(exclude=("test")),
    include_package_data=True,
    install_requires=[
        'asyncio',
        'aiohttp'
    ],
)