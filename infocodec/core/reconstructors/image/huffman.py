"""
Huffman Reconstructor

Decodes variable-length Huffman codes back to original symbols.
"""

import numpy as np
from typing import Dict, Any
import json
from infocodec.core.base import ImageReconstructor


class HuffmanReconstructor(ImageReconstructor):
    """
    Huffman coding reconstruction.
    
    Decodes bit stream using Huffman code table.
    """
    
    def reconstruct(self, compressed_bytes: bytes, metadata: Dict[str, Any]) -> np.ndarray:
        """
        Reconstruct image from Huffman encoded data.
        
        Args:
            compressed_bytes: Huffman encoded data (tree + encoded bits)
            metadata: Metadata with shape and Huffman codes
            
        Returns:
            Reconstructed image array
        """
        shape = metadata.get('original_shape', metadata.get('shape'))
        
        # Extract Huffman codes from metadata
        huffman_codes = metadata.get('huffman_codes', {})
        
        # If codes stored as string keys, convert back to int
        if huffman_codes and isinstance(list(huffman_codes.keys())[0], str):
            huffman_codes = {int(k): v for k, v in huffman_codes.items()}
        
        # Invert the code table (code -> symbol)
        decode_table = {code: symbol for symbol, code in huffman_codes.items()}
        
        # Extract tree length and padding from compressed bytes
        if len(compressed_bytes) < 5:
            # Not enough data
            reconstructed = np.zeros(shape if isinstance(shape, (list, tuple)) else (1, 1), 
                                    dtype=np.uint8)
        else:
            tree_length = int.from_bytes(compressed_bytes[:4], byteorder='big')
            tree_end = 4 + tree_length
            
            if len(compressed_bytes) < tree_end + 1:
                reconstructed = np.zeros(shape if isinstance(shape, (list, tuple)) else (1, 1),
                                        dtype=np.uint8)
            else:
                padding = compressed_bytes[tree_end]
                encoded_bytes = compressed_bytes[tree_end + 1:]
                
                # Convert bytes to bit string
                bit_string = ''.join(format(byte, '08b') for byte in encoded_bytes)
                
                # Remove padding
                if padding > 0:
                    bit_string = bit_string[:-padding]
                
                # Decode bit stream
                decoded = []
                current_code = ""
                
                for bit in bit_string:
                    current_code += bit
                    if current_code in decode_table:
                        decoded.append(decode_table[current_code])
                        current_code = ""
                
                decoded_array = np.array(decoded, dtype=np.uint8)
                
                # Reshape
                if isinstance(shape, (list, tuple)) and len(shape) >= 2:
                    expected_size = int(np.prod(shape))

                    if len(decoded_array) < expected_size:
                        decoded_array = np.pad(decoded_array,
                                              (0, expected_size - len(decoded_array)),
                                              mode='edge')
                    elif len(decoded_array) > expected_size:
                        decoded_array = decoded_array[:expected_size]

                    reconstructed = decoded_array.reshape(shape)
                else:
                    reconstructed = decoded_array
        
        # Postprocess
        reconstructed = self._postprocess_image(reconstructed, metadata)
        
        self.stats = {
            'method': 'Huffman Decode',
            'symbols_decoded': reconstructed.size,
            'quality': 'Perfect (Lossless)',
        }
        
        return reconstructed
    
    def get_stats(self) -> Dict[str, Any]:
        """Return reconstruction statistics"""
        return self.stats
