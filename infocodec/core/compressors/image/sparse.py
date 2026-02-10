"""
Sparse Sampling Compressor

Samples a subset of pixels and stores their positions.
Reconstruction uses interpolation to fill missing values.
"""

import numpy as np
from typing import Dict, Any, Tuple
import struct
from infocodec.core.base import ImageCompressor
from infocodec.core.metrics import calculate_entropy


class SparseCompressor(ImageCompressor):
    """
    Sparse sampling compression.
    
    Best for: Quick previews, extreme bandwidth constraints
    Compression: 10-50x depending on sampling rate
    Type: Lossy (interpolation-based reconstruction)
    """
    
    def __init__(self, sampling_rate: int = 4, **kwargs):
        """
        Initialize sparse compressor.
        
        Args:
            sampling_rate: Sample every Nth pixel (e.g., 4 = every 4th pixel)
        """
        super().__init__(**kwargs)
        self.sampling_rate = sampling_rate
    
    def compress(self, data: np.ndarray) -> Tuple[bytes, Dict[str, Any]]:
        """
        Compress image using sparse sampling.
        
        Args:
            data: Input image array
            
        Returns:
            compressed_bytes: Sparse sampled pixels + positions
            metadata: Image dimensions and sampling info
        """
        # Preprocess
        image = self._preprocess_image(data)
        height, width = image.shape
        
        # Sample pixels
        sampled_pixels = []
        sampled_positions = []
        
        for i in range(0, height, self.sampling_rate):
            for j in range(0, width, self.sampling_rate):
                sampled_pixels.append(image[i, j])
                sampled_positions.append((i, j))
        
        # Convert to bytes
        # Format: [num_samples(4)][sample1_row(2)][sample1_col(2)][sample1_val(1)]...
        num_samples = len(sampled_pixels)
        compressed_data = [struct.pack('>I', num_samples)]
        
        for (row, col), pixel in zip(sampled_positions, sampled_pixels):
            compressed_data.append(struct.pack('>HHB', row, col, pixel))
        
        compressed_bytes = b''.join(compressed_data)
        
        # Calculate stats
        original_size = height * width
        sparsity = num_samples / original_size if original_size > 0 else 0
        
        self.stats = {
            'method': 'Sparse',
            'original_pixels': original_size,
            'sampled_pixels': num_samples,
            'compressed_bytes': len(compressed_bytes),
            'sampling_rate': self.sampling_rate,
            'sparsity': sparsity,
            'compression_ratio': original_size / num_samples if num_samples > 0 else float('inf'),
            'space_saved_percent': (1 - sparsity) * 100,
            'entropy': calculate_entropy(image),
        }
        
        # Metadata
        metadata = self._create_metadata()
        metadata.update({
            'original_shape': image.shape,
            'sampling_rate': self.sampling_rate,
            'num_samples': num_samples,
            'sampled_positions': sampled_positions,  # For reconstruction
        })
        
        return compressed_bytes, metadata
    
    def get_stats(self) -> Dict[str, Any]:
        """Return compression statistics"""
        return self.stats
