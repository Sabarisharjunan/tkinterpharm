from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tkinterpharm",
    version="1.0.0",
    author="Sabarisharjunan",
    description="Enterprise-grade Pharmacy Management System built with Tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sabarisharjunan/tkinterpharm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.11",
    install_requires=[
        "SQLAlchemy>=2.0.23",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0.1",
        "bcrypt>=4.1.1",
        "pandas>=2.1.3",
        "openpyxl>=3.10.10",
        "Pillow>=10.1.0",
    ],
)
