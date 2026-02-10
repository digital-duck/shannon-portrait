"""
DCT Reconstructor

Reconstructs image from DCT coefficients (JPEG-style).
"""

import numpy as np
from typing import Dict, Any
from scipy.fftpack import idct
from infocodec.core.base import ImageReconstructor


class DCTReconstructor(ImageReconstructor):
    """
    DCT-based reconstruction (JPEG-style).
    
    Applies inverse DCT to frequency-domain coefficients.
    """
    
    def reconstruct(self, compressed_bytes: bytes, metadata: Dict[str, Any]) -> np.ndarray:
        """
        Reconstruct image from DCT coefficients.
        
        Args:
            compressed_bytes: DCT coefficients
            metadata: Metadata with shape and DCT parameters
            
        Returns:
            Reconstructed image array (lossy if quantized)
        """
        shape = metadata.get('original_shape', metadata.get('shape'))
        padded_shape = metadata.get('padded_shape', shape)
        block_size = metadata.get('block_size', 8)
        quality = metadata.get('quality', 0.8)
        
        if not isinstance(shape, (list, tuple)) or len(shape) < 2:
            return np.zeros((1, 1), dtype=np.uint8)
        
        height, width = shape[0], shape[1]
        padded_h, padded_w = padded_shape[0], padded_shape[1]
        
        # Convert bytes back to float32 coefficients
        all_coeffs = np.frombuffer(compressed_bytes, dtype=np.float32)
        
        # Calculate number of blocks
        num_blocks = (padded_h // block_size) * (padded_w // block_size)
        coeffs_per_block = block_size * block_size
        
        # Reconstruct each block
        reconstructed_padded = np.zeros((padded_h, padded_w), dtype=np.float32)
        
        block_idx = 0
        for i in range(0, padded_h, block_size):
            for j in range(0, padded_w, block_size):
                if block_idx >= num_blocks:
                    break
                
                # Extract block coefficients
                start_idx = block_idx * coeffs_per_block
                end_idx = start_idx + coeffs_per_block
                
                if end_idx <= len(all_coeffs):
                    block_coeffs = all_coeffs[start_idx:end_idx].reshape(block_size, block_size)
                    
                    # Dequantize
                    dequantized = self._dequantize(block_coeffs, quality, block_size)
                    
                    # Inverse DCT
                    reconstructed_block = idct(idct(dequantized.T, norm='ortho').T, norm='ortho')
                    
                    # Clip and place in image
                    reconstructed_block = np.clip(reconstructed_block, 0, 255)
                    reconstructed_padded[i:i+block_size, j:j+block_size] = reconstructed_block
                
                block_idx += 1
        
        # Remove padding
        reconstructed = reconstructed_padded[:height, :width].astype(np.uint8)
        
        # Postprocess
        reconstructed = self._postprocess_image(reconstructed, metadata)
        
        self.stats = {
            'method': 'DCT Reconstruction',
            'blocks_processed': block_idx,
            'quality': quality,
            'quality_level': 'Lossy' if quality < 1.0 else 'High Quality',
        }
        
        return reconstructed
    
    def _dequantize(self, quantized_block: np.ndarray, quality: float, block_size: int) -> np.ndarray:
        """
        Reverse quantization.
        
        Args:
            quantized_block: Quantized DCT coefficients
            quality: Quality factor used in compression
            block_size: Size of DCT block
            
        Returns:
            Dequantized coefficients
        """
        scale = 1.0 / quality
        
        # Reconstruct quantization matrix
        quant_matrix = np.zeros_like(quantized_block)
        for i in range(block_size):
            for j in range(block_size):
                dist = i + j
                quant_matrix[i, j] = 1.0 + dist * scale
        
        # Dequantize
        dequantized = quantized_block * quant_matrix
        
        return dequantized
    
    def get_stats(self) -> Dict[str, Any]:
        """Return reconstruction statistics"""
        return self.stats
