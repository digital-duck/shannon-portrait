"""Image compression methods"""

from infocodec.core.compressors.image.naive import NaiveCompressor
from infocodec.core.compressors.image.rle import RLECompressor
from infocodec.core.compressors.image.differential import DifferentialCompressor
from infocodec.core.compressors.image.huffman import HuffmanCompressor
from infocodec.core.compressors.image.sparse import SparseCompressor
from infocodec.core.compressors.image.dct import DCTCompressor

__all__ = [
    "NaiveCompressor",
    "RLECompressor",
    "DifferentialCompressor",
    "HuffmanCompressor",
    "SparseCompressor",
    "DCTCompressor",
]

# Registry for easy lookup
COMPRESSORS = {
    'naive': NaiveCompressor,
    'rle': RLECompressor,
    'differential': DifferentialCompressor,
    'huffman': HuffmanCompressor,
    'sparse': SparseCompressor,
    'dct': DCTCompressor,
}
