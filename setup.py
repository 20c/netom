
from setuptools import find_packages, setup


def read_file(name):
    with open(name) as fobj:
        return fobj.read().strip()

LONG_DESCRIPTION = read_file("README.md")
VERSION = read_file("Ctl/VERSION")
REQUIREMENTS = read_file("Ctl/requirements.txt").split("\n")
TEST_REQUIREMENTS = read_file("Ctl/requirements-test.txt").split("\n")


setup(
    name="netom",
    version=VERSION,
    author="20C",
    author_email="code@20c.com",
    description="Network object models",
    long_description=LONG_DESCRIPTION,
    license="LICENSE.txt",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    packages=find_packages("src"),
    package_dir={"": "src"},


    include_package_data=True,
    url="https://github.com/20c/netom",
    download_url="https://github.com/20c/netom/%s" % VERSION,

    install_requires=REQUIREMENTS,
    test_requires=TEST_REQUIREMENTS,

    entry_points={
        'console_scripts': [
            'netom=netom.__main__:main',
        ]
    },

    zip_safe=True
)
