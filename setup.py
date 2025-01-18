# setup.py

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pushpit-kamboj-102203281",  # Replace with your "Topsis-FirstName-RollNumber"
    version="0.0.1",
    author="Shyam",
    author_email="pushpitkamboj@gmail.com",
    description="A Python package for TOPSIS analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pushpitkamboj/pushpit-kamboj-102203281",  # optional, if you have a public repo
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            # the left side is the command (e.g. "topsis") you want to run in terminal
            # the right side is "packageName.moduleName:functionName"
            "topsis = pushpit_kamboj_102203281.topsis:main"
        ]
    },
    python_requires='>=3.6',
)
