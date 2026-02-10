"""
Shannon Portrait - InfoCodec Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="shannon-portrait",
    version="0.1.0",
    author="Shannon Portrait Project",
    author_email="info@shannon-portrait.org",
    description="Information Coding & Encoding - Research tool for Shannon's Information Theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shannon-portrait",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "Pillow>=9.0.0",
        "click>=8.0.0",
        "rich>=10.0.0",
        "streamlit>=1.28.0",
        "plotly>=5.0.0",
        "openai>=1.0.0",  # For OpenRouter API
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "audio": [
            "librosa>=0.9.0",
            "soundfile>=0.11.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "infocodec=infocodec.cli:cli",
        ],
    },
    package_data={
        "infocodec": [
            "ui/pages/*.py",
            "ui/components/*.py",
            "data/images/*.png",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
