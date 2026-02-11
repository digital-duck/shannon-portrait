"""
Huffman Coding Compressor

Variable-length encoding based on symbol frequency.
Approaches Shannon entropy limit for symbol-by-symbol encoding.
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional
import struct
import heapq
import json
from infocodec.core.base import ImageCompressor
from infocodec.core.metrics import calculate_entropy


class HuffmanNode:
    """Node in Huffman tree"""
    def __init__(self, freq: int, symbol: Optional[int] = None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCompressor(ImageCompressor):
    """
    Huffman coding compression.
    
    Best for: General purpose, approaches entropy limit
    Compression: 1.5-3x depending on entropy
    Type: Lossless
    Efficiency: 97-99% of theoretical limit
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.huffman_tree = None
        self.huffman_codes = {}
    
    def compress(self, data: np.ndarray) -> Tuple[bytes, Dict[str, Any]]:
        """
        Compress image using Huffman coding.
        
        Args:
            data: Input image array
            
        Returns:
            compressed_bytes: Huffman encoded data + tree
            metadata: Image dimensions and stats
        """
        # Preprocess
        image = self._preprocess_image(data)
        flat_data = image.flatten()
        
        if len(flat_data) == 0:
            compressed_bytes = b''
            self.huffman_codes = {}
        else:
            # Build frequency table
            values, counts = np.unique(flat_data, return_counts=True)
            freq_dict = dict(zip(values.astype(int), counts.astype(int)))
            
            # Build Huffman tree
            self._build_huffman_tree(freq_dict)
            
            # Generate codes
            self._generate_codes(self.huffman_tree)
            
            # Encode data
            encoded_bits = ''.join(self.huffman_codes[int(val)] for val in flat_data)
            
            # Convert bits to bytes (pad to byte boundary)
            padding = (8 - len(encoded_bits) % 8) % 8
            encoded_bits += '0' * padding
            
            # Convert bit string to bytes
            encoded_bytes = int(encoded_bits, 2).to_bytes(len(encoded_bits) // 8, byteorder='big')
            
            # Serialize Huffman tree (as code table)
            tree_json = json.dumps(self.huffman_codes)
            tree_bytes = tree_json.encode('utf-8')
            
            # Format: [tree_length(4)][tree][padding(1)][encoded_data]
            compressed_bytes = (
                len(tree_bytes).to_bytes(4, byteorder='big') +
                tree_bytes +
                padding.to_bytes(1, byteorder='big') +
                encoded_bytes
            )
        
        # Calculate stats
        original_entropy = calculate_entropy(image)
        avg_code_length = sum(len(self.huffman_codes[int(val)]) * count 
                             for val, count in zip(values, counts)) / len(flat_data) if self.huffman_codes else 0
        
        self.stats = {
            'method': 'Huffman',
            'original_pixels': len(flat_data),
            'compressed_bytes': len(compressed_bytes),
            'num_symbols': len(self.huffman_codes),
            'entropy': original_entropy,
            'avg_code_length': avg_code_length,
            'efficiency': (original_entropy / avg_code_length * 100) if avg_code_length > 0 else 0,
            'compression_ratio': (len(flat_data) * 8) / len(compressed_bytes) if len(compressed_bytes) > 0 else float('inf'),
            'bits_per_pixel': len(compressed_bytes) * 8 / len(flat_data) if len(flat_data) > 0 else 0,
        }
        
        # Metadata
        metadata = self._create_metadata()
        metadata.update({
            'original_shape': image.shape,
            'huffman_codes': self.huffman_codes,
            'num_symbols': len(self.huffman_codes),
        })
        
        return compressed_bytes, metadata
    
    def _build_huffman_tree(self, freq_dict: Dict[int, int]):
        """Build Huffman tree from frequency dictionary"""
        if not freq_dict:
            self.huffman_tree = None
            return
        
        # Create leaf nodes
        heap = [HuffmanNode(freq, symbol) for symbol, freq in freq_dict.items()]
        heapq.heapify(heap)
        
        # Build tree
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            parent = HuffmanNode(left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, parent)
        
        self.huffman_tree = heap[0] if heap else None
    
    def _generate_codes(self, node: Optional[HuffmanNode], code: str = ""):
        """Generate Huffman codes from tree"""
        if node is None:
            return
        
        if node.symbol is not None:
            # Leaf node — cast to native int so keys are JSON-serialisable
            self.huffman_codes[int(node.symbol)] = code if code else "0"
        else:
            # Internal node
            if node.left:
                self._generate_codes(node.left, code + "0")
            if node.right:
                self._generate_codes(node.right, code + "1")
    
    def get_stats(self) -> Dict[str, Any]:
        """Return compression statistics"""
        return self.stats
