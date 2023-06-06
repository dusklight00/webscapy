from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="webscapy",
    version="1.5.5",
    description="Selenium built for scraping instead of testing",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Rahul Raj",
    packages=["webscapy"],
    zip_safe=False,
    project_urls={
        "Documentation": "https://pypi.org/project/webscapy/",
        "Source": "https://pypi.org/project/webscapy/",
    },
    install_requires=[
        "selenium",
        "webdriver_manager",
        "uc-browser"
    ]
)