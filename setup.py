"""إعداد حزمة المشروع"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="RAG-OKLENT01",
    version="0.1.0",
    author="OKLENT2024",
    description="Retrieval-Augmented Generation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OKLENT2024/RAG-OKLENT01",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
