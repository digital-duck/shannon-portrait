"""
InfoCodec - Information Coding and Encoding
============================================

A research and educational tool for exploring Shannon's Information Theory
through practical image compression and reconstruction.

Based on Claude Shannon's seminal work on information theory.
"""

__version__ = "0.1.0"
__author__ = "Shannon Portrait Project"

from infocodec.core.base import Compressor, Reconstructor
from infocodec.core.metrics import calculate_entropy, calculate_psnr, calculate_compression_ratio

__all__ = [
    "Compressor",
    "Reconstructor", 
    "calculate_entropy",
    "calculate_psnr",
    "calculate_compression_ratio",
]
