from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ghdorker",
    version='0.3.1',
    author="David Tippett",
    author_email="dtaivpp@gmail.com",
    description="A better GitHub Dorking Utility",
    license='Apache Software License',
    license_files=['LICENSE'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="GitHub Dorker Python Security Dorking",
    url="https://github.com/dtaivpp/gh-dorker",
    packages=['GHDorker'],
    install_requires=['ghapi','python-dotenv', 'wheel'],
    entry_points = {
        'console_scripts': ['ghdorker=GHDorker.dorker:cli_entry'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent"
    ],
)
