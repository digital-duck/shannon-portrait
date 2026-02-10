"""Image reconstruction methods"""

from infocodec.core.reconstructors.image.direct import DirectReconstructor
from infocodec.core.reconstructors.image.rle import RLEReconstructor
from infocodec.core.reconstructors.image.differential import DifferentialReconstructor
from infocodec.core.reconstructors.image.huffman import HuffmanReconstructor
from infocodec.core.reconstructors.image.sparse import SparseReconstructor
from infocodec.core.reconstructors.image.dct import DCTReconstructor

__all__ = [
    "DirectReconstructor",
    "RLEReconstructor",
    "DifferentialReconstructor",
    "HuffmanReconstructor",
    "SparseReconstructor",
    "DCTReconstructor",
]

# Registry for easy lookup
RECONSTRUCTORS = {
    'naive': DirectReconstructor,
    'direct': DirectReconstructor,
    'rle': RLEReconstructor,
    'differential': DifferentialReconstructor,
    'huffman': HuffmanReconstructor,
    'sparse': SparseReconstructor,
    'dct': DCTReconstructor,
}
