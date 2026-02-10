"""
Unit Tests for Compression Algorithms

Tests all 6 compression methods with various image patterns.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from infocodec.core.compressors import COMPRESSORS
from infocodec.utils.image_utils import create_test_image


class TestCompressors:
    """Test suite for all compression algorithms"""
    
    @pytest.fixture
    def test_images(self):
        """Generate test images with different characteristics"""
        return {
            'gradient': create_test_image(size=(64, 64), pattern='gradient'),
            'blocks': create_test_image(size=(64, 64), pattern='blocks'),
            'noise': create_test_image(size=(64, 64), pattern='noise'),
            'checkerboard': create_test_image(size=(64, 64), pattern='checkerboard'),
            'small': create_test_image(size=(16, 16), pattern='gradient'),
            'large': create_test_image(size=(128, 128), pattern='blocks'),
        }
    
    def test_all_compressors_exist(self):
        """Test that all expected compressors are registered"""
        expected_methods = ['naive', 'rle', 'differential', 'huffman', 'sparse', 'dct']
        
        for method in expected_methods:
            assert method in COMPRESSORS, f"Compressor '{method}' not found in registry"
    
    def test_naive_compressor(self, test_images):
        """Test naive compressor on various images"""
        compressor = COMPRESSORS['naive']()
        
        for name, image in test_images.items():
            compressed_bytes, metadata = compressor.compress(image)
            stats = compressor.get_stats()
            
            # Verify basic properties
            assert isinstance(compressed_bytes, bytes), f"Naive/{name}: Output should be bytes"
            assert len(compressed_bytes) > 0, f"Naive/{name}: Compressed data is empty"
            assert 'method' in metadata, f"Naive/{name}: Missing method in metadata"
            assert metadata['method'] == 'Naive', f"Naive/{name}: Wrong method in metadata"
            assert stats['compression_ratio'] == 1.0, f"Naive/{name}: Should have 1.0x ratio"
    
    def test_rle_compressor(self, test_images):
        """Test RLE compressor"""
        compressor = COMPRESSORS['rle']()
        
        # RLE should compress blocks very well
        compressed_bytes, metadata = compressor.compress(test_images['blocks'])
        stats = compressor.get_stats()
        
        assert isinstance(compressed_bytes, bytes), "RLE: Output should be bytes"
        assert stats['compression_ratio'] > 2.0, "RLE: Should compress blocks >2x"
        
        # RLE should expand noise
        compressed_bytes, metadata = compressor.compress(test_images['noise'])
        stats = compressor.get_stats()
        
        assert stats['compression_ratio'] < 1.0, "RLE: Should expand noise"
    
    def test_differential_compressor(self, test_images):
        """Test differential compressor"""
        compressor = COMPRESSORS['differential']()
        
        # Differential should work well on gradients
        compressed_bytes, metadata = compressor.compress(test_images['gradient'])
        stats = compressor.get_stats()
        
        assert isinstance(compressed_bytes, bytes), "Differential: Output should be bytes"
        assert stats['entropy_reduction'] > 50, "Differential: Should reduce entropy >50% on gradients"
        
        # Test metadata
        assert 'max_diff' in metadata, "Differential: Missing max_diff in metadata"
        assert 'bits_per_symbol' in metadata, "Differential: Missing bits_per_symbol"
    
    def test_huffman_compressor(self, test_images):
        """Test Huffman compressor"""
        compressor = COMPRESSORS['huffman']()
        
        for name, image in test_images.items():
            compressed_bytes, metadata = compressor.compress(image)
            stats = compressor.get_stats()
            
            # Verify Huffman properties
            assert isinstance(compressed_bytes, bytes), f"Huffman/{name}: Output should be bytes"
            assert 'huffman_codes' in metadata, f"Huffman/{name}: Missing codes in metadata"
            assert stats['efficiency'] > 90, f"Huffman/{name}: Efficiency should be >90%"
            assert 'avg_code_length' in stats, f"Huffman/{name}: Missing avg_code_length"
    
    def test_sparse_compressor(self, test_images):
        """Test sparse compressor"""
        compressor = COMPRESSORS['sparse'](sampling_rate=4)
        
        compressed_bytes, metadata = compressor.compress(test_images['gradient'])
        stats = compressor.get_stats()
        
        assert isinstance(compressed_bytes, bytes), "Sparse: Output should be bytes"
        assert stats['compression_ratio'] > 10, "Sparse: Should compress >10x"
        assert 'sampled_positions' in metadata, "Sparse: Missing positions in metadata"
        assert stats['sparsity'] < 0.1, "Sparse: Sparsity should be <0.1 for rate=4"
    
    def test_dct_compressor(self, test_images):
        """Test DCT compressor"""
        compressor = COMPRESSORS['dct'](block_size=8, quality=0.8)
        
        compressed_bytes, metadata = compressor.compress(test_images['gradient'])
        stats = compressor.get_stats()
        
        assert isinstance(compressed_bytes, bytes), "DCT: Output should be bytes"
        assert 'block_size' in metadata, "DCT: Missing block_size in metadata"
        assert 'quality' in metadata, "DCT: Missing quality in metadata"
        assert metadata['quality'] == 0.8, "DCT: Quality not preserved in metadata"
    
    def test_compression_ratio_ordering(self, test_images):
        """Test that compression ratios make sense for different patterns"""
        blocks_image = test_images['blocks']
        
        # RLE should be best for blocks
        rle = COMPRESSORS['rle']()
        rle_bytes, _ = rle.compress(blocks_image)
        rle_ratio = rle.get_stats()['compression_ratio']
        
        # Huffman should be moderate
        huffman = COMPRESSORS['huffman']()
        huffman_bytes, _ = huffman.compress(blocks_image)
        huffman_ratio = huffman.get_stats()['compression_ratio']
        
        # Naive should be 1.0
        naive = COMPRESSORS['naive']()
        naive_bytes, _ = naive.compress(blocks_image)
        naive_ratio = naive.get_stats()['compression_ratio']
        
        assert rle_ratio > huffman_ratio, "RLE should compress blocks better than Huffman"
        assert huffman_ratio >= naive_ratio, "Huffman should be at least as good as naive"
    
    def test_metadata_completeness(self, test_images):
        """Test that all compressors return complete metadata"""
        required_fields = ['shape', 'method']
        
        for method_name, compressor_class in COMPRESSORS.items():
            compressor = compressor_class()
            _, metadata = compressor.compress(test_images['gradient'])
            
            for field in required_fields:
                assert field in metadata or 'original_shape' in metadata, \
                    f"{method_name}: Missing required field '{field}' in metadata"
    
    def test_empty_image(self):
        """Test handling of edge cases"""
        # This should handle gracefully or raise appropriate error
        empty = np.array([], dtype=np.uint8).reshape(0, 0)
        
        for method_name, compressor_class in COMPRESSORS.items():
            try:
                compressor = compressor_class()
                compressed_bytes, metadata = compressor.compress(empty)
                # If it doesn't raise an error, verify it returns something reasonable
                assert isinstance(compressed_bytes, bytes), f"{method_name}: Should return bytes even for empty"
            except (ValueError, IndexError):
                # It's okay to raise an error for empty images
                pass
    
    def test_single_pixel(self):
        """Test single pixel image"""
        single = np.array([[128]], dtype=np.uint8)
        
        for method_name, compressor_class in COMPRESSORS.items():
            compressor = compressor_class()
            compressed_bytes, metadata = compressor.compress(single)
            stats = compressor.get_stats()
            
            assert isinstance(compressed_bytes, bytes), f"{method_name}: Should handle single pixel"
            assert 'method' in metadata, f"{method_name}: Should have method in metadata"


class TestCompressionProperties:
    """Test theoretical properties of compression"""
    
    def test_entropy_bounds(self):
        """Test that entropy calculations are within valid bounds"""
        from infocodec.core.metrics import calculate_entropy
        
        # Test various images
        images = {
            'uniform': np.full((64, 64), 128, dtype=np.uint8),  # Should have 0 entropy
            'binary': np.random.choice([0, 255], size=(64, 64)).astype(np.uint8),  # Should have ~1 bit
            'random': np.random.randint(0, 256, size=(64, 64), dtype=np.uint8),  # Should have ~8 bits
        }
        
        for name, image in images.items():
            entropy = calculate_entropy(image)
            assert 0 <= entropy <= 8, f"{name}: Entropy should be between 0 and 8 bits"
    
    def test_compression_lossless_property(self):
        """Test that lossless methods can be perfectly reconstructed"""
        from infocodec.core.reconstructors import RECONSTRUCTORS
        
        test_image = create_test_image(size=(32, 32), pattern='gradient')
        
        lossless_methods = ['naive', 'rle', 'differential', 'huffman']
        
        for method in lossless_methods:
            compressor = COMPRESSORS[method]()
            reconstructor = RECONSTRUCTORS[method]()
            
            compressed_bytes, metadata = compressor.compress(test_image)
            reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
            
            # For lossless, should be identical
            if method in ['naive', 'rle', 'differential', 'huffman']:
                assert np.array_equal(test_image, reconstructed), \
                    f"{method}: Lossless compression should allow perfect reconstruction"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
