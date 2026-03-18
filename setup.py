"""
Setup script for French-Wolof Translator package.
"""
from setuptools import setup, find_packages
from version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="french-wolof-translator",
    version=__version__,
    author="GalsenAI",
    description="A modular French-Wolof translation system using NLLB models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galsenai/french-wolof-translator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "french-wolof-translate=main:main",
            "french-wolof-train=train:main",
        ],
    },
)

