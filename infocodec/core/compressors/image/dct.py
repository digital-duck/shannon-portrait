"""
DCT (Discrete Cosine Transform) Compressor

Transform-based compression similar to JPEG.
Converts spatial domain to frequency domain, quantizes high frequencies.
"""

import numpy as np
from typing import Dict, Any, Tuple
from scipy.fftpack import dct, idct
from infocodec.core.base import ImageCompressor
from infocodec.core.metrics import calculate_entropy


class DCTCompressor(ImageCompressor):
    """
    DCT-based compression (JPEG-style).
    
    Best for: Natural photos with smooth variations
    Compression: 5-20x depending on quality
    Type: Lossy (frequency-domain quantization)
    """
    
    def __init__(self, block_size: int = 8, quality: float = 0.8, **kwargs):
        """
        Initialize DCT compressor.
        
        Args:
            block_size: Size of DCT blocks (typically 8x8)
            quality: Quality factor 0.0-1.0 (1.0 = best quality, least compression)
        """
        super().__init__(**kwargs)
        self.block_size = block_size
        self.quality = max(0.1, min(1.0, quality))  # Clamp to [0.1, 1.0]
    
    def compress(self, data: np.ndarray) -> Tuple[bytes, Dict[str, Any]]:
        """
        Compress image using DCT.
        
        Args:
            data: Input image array
            
        Returns:
            compressed_bytes: DCT coefficients
            metadata: Image dimensions and DCT parameters
        """
        # Preprocess
        image = self._preprocess_image(data)
        height, width = image.shape
        
        # Pad image to multiple of block_size
        pad_h = (self.block_size - height % self.block_size) % self.block_size
        pad_w = (self.block_size - width % self.block_size) % self.block_size
        
        if pad_h > 0 or pad_w > 0:
            padded = np.pad(image, ((0, pad_h), (0, pad_w)), mode='edge')
        else:
            padded = image
        
        padded_h, padded_w = padded.shape
        
        # Process in blocks
        dct_blocks = []
        for i in range(0, padded_h, self.block_size):
            for j in range(0, padded_w, self.block_size):
                block = padded[i:i+self.block_size, j:j+self.block_size].astype(np.float32)
                
                # Apply 2D DCT
                dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
                
                # Apply quality-based quantization
                quantized = self._quantize(dct_block)
                
                dct_blocks.append(quantized)
        
        # Flatten all DCT blocks
        all_coeffs = np.concatenate([block.flatten() for block in dct_blocks])
        
        # Convert to bytes (using float32)
        compressed_bytes = all_coeffs.astype(np.float32).tobytes()
        
        # Calculate stats
        original_size = height * width * 1  # 1 byte per pixel
        compressed_size = len(compressed_bytes)
        
        self.stats = {
            'method': 'DCT',
            'original_pixels': height * width,
            'compressed_bytes': compressed_size,
            'block_size': self.block_size,
            'quality': self.quality,
            'num_blocks': len(dct_blocks),
            'compression_ratio': original_size / compressed_size if compressed_size > 0 else float('inf'),
            'padded_shape': (padded_h, padded_w),
            'entropy': calculate_entropy(image),
        }
        
        # Metadata
        metadata = self._create_metadata()
        metadata.update({
            'original_shape': (height, width),
            'padded_shape': (padded_h, padded_w),
            'block_size': self.block_size,
            'quality': self.quality,
            'num_blocks': len(dct_blocks),
        })
        
        return compressed_bytes, metadata
    
    def _quantize(self, dct_block: np.ndarray) -> np.ndarray:
        """
        Quantize DCT coefficients based on quality.
        
        Higher frequencies are quantized more aggressively.
        """
        # Create quantization matrix (simplified)
        # Higher quality = less quantization
        scale = 1.0 / self.quality
        
        # Zigzag-ordered quantization strength
        # Low frequencies preserved more
        quant_matrix = np.zeros_like(dct_block)
        for i in range(self.block_size):
            for j in range(self.block_size):
                # Distance from DC coefficient
                dist = i + j
                quant_matrix[i, j] = 1.0 + dist * scale
        
        # Quantize
        quantized = dct_block / quant_matrix
        
        # Zero out small coefficients
        threshold = np.max(np.abs(quantized)) * (1.0 - self.quality) * 0.1
        quantized[np.abs(quantized) < threshold] = 0
        
        return quantized
    
    def get_stats(self) -> Dict[str, Any]:
        """Return compression statistics"""
        return self.stats
