from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="webscapy",
    version="1.2.1",
    description="Selenium built for scraping instead of testing",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Rahul Raj",
    packages=["webscapy"],
    zip_safe=False
)