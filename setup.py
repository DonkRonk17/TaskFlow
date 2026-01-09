#!/usr/bin/env python3
"""
Setup script for TaskFlow
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="taskflow",
    version="1.0.0",
    description="Smart CLI todo and project manager - lightweight, git-friendly task tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Holy Grail Automation",
    author_email="",
    url="https://github.com/DonkRonk17/TaskFlow",
    py_modules=["taskflow"],
    install_requires=[
        # Zero dependencies!
    ],
    entry_points={
        "console_scripts": [
            "taskflow=taskflow:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Project Management",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="todo task management cli productivity git-friendly developer-tools",
)
