import setuptools
import os
import io


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="PyAwnfra",
    version="0.0.1",
    description="An AWS CDK Library for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Guy Wilson",
    author_email="guywilsonjr@gmail.com",
    url="https://github.com/guywilsonjr/PyAwnfra",
    python_requires=">=3.6",

    packages=setuptools.find_packages(),

    install_requires=[
        "aws-cdk.core",
    ],
    keywords='infrastructure aws',

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
