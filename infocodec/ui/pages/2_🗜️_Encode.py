"""
Encode Page
===========

Upload and compress images using various compression methods.
"""

import streamlit as st
import numpy as np
from PIL import Image
import io
import time
from pathlib import Path

from infocodec.core.compressors import COMPRESSORS
from infocodec.core.metrics import calculate_entropy, comprehensive_quality_analysis
from infocodec.utils.image_utils import create_test_image
from infocodec.utils.paths import make_output_filename, quality_qualifier, sampling_rate_qualifier

st.set_page_config(page_title="Encode - InfoCodec", page_icon="🗜️", layout="wide")

st.title("🗜️ Encode (Compress)")
st.markdown("Upload an image and compress it using various methods.")

# Initialize session state
if 'encoded_data' not in st.session_state:
    st.session_state.encoded_data = {}

if 'settings' not in st.session_state:
    st.session_state.settings = {
        'compression_method': 'auto',
        'quality_level': 1.0,
        'block_size': 8,
    }

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 Input")
    
    # Image source selection
    source = st.radio(
        "Image Source",
        options=["Upload Image", "Generate Test Pattern"],
        horizontal=True
    )
    
    original_image = None
    
    if source == "Upload Image":
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'bmp'],
            help="Upload a PNG, JPG, or BMP image"
        )

        if uploaded_file is not None:
            # Load image
            image_pil = Image.open(uploaded_file)

            # Normalise to RGB; keep native grayscale as-is
            if image_pil.mode == 'L':
                original_image = np.array(image_pil, dtype=np.uint8)
            else:
                original_image = np.array(image_pil.convert('RGB'), dtype=np.uint8)
            # Track input stem for output filename derivation
            st.session_state['input_stem'] = Path(uploaded_file.name).stem

            st.success(f"✅ Loaded: {original_image.shape[0]}×{original_image.shape[1]} pixels")

    else:  # Generate Test Pattern
        pattern = st.selectbox(
            "Pattern Type",
            options=['gradient', 'blocks', 'noise', 'checkerboard'],
            help="Different patterns have different compression characteristics"
        )

        size = st.slider("Image Size", min_value=32, max_value=256, value=128, step=32)

        if st.button("🎨 Generate Pattern"):
            original_image = create_test_image(size=(size, size), pattern=pattern)
            st.session_state['input_stem'] = f"test_{pattern}_{size}x{size}"
            st.success(f"✅ Generated {pattern} pattern: {size}×{size} pixels")
    
    # Display original image
    if original_image is not None:
        st.subheader("Original Image")
        st.image(original_image, use_column_width=True, clamp=True)
        
        # Image info
        with st.expander("📊 Image Information"):
            entropy = calculate_entropy(original_image)
            st.metric("Entropy", f"{entropy:.3f} bits/pixel")
            st.metric("Size", f"{original_image.shape[0]}×{original_image.shape[1]}")
            st.metric("Total Pixels", f"{original_image.size:,}")
            st.metric("Unique Values", f"{len(np.unique(original_image))}")
            st.metric("Min/Max", f"{np.min(original_image)} / {np.max(original_image)}")
            
            # Distribution
            st.markdown("**Pixel Value Distribution**")
            hist_values = np.histogram(original_image, bins=50)[0]
            st.bar_chart(hist_values)

with col2:
    st.header("⚙️ Compression Settings")
    
    if original_image is not None:
        # Method selection
        method = st.selectbox(
            "Compression Method",
            options=['auto', 'naive', 'rle', 'differential', 'huffman', 'sparse', 'dct'],
            index=0,
            help="Auto-detection analyzes the image and selects the best method"
        )
        
        # Method-specific parameters
        if method == 'sparse':
            sampling_rate = st.slider("Sampling Rate (every Nth pixel)", 
                                     min_value=2, max_value=8, value=4)
        elif method == 'dct':
            quality = st.slider("Quality", min_value=0.1, max_value=1.0, 
                               value=0.8, step=0.1,
                               help="Higher = better quality, lower compression")
        else:
            quality = st.session_state.settings['quality_level']
            sampling_rate = 4
        
        # Compress button
        if st.button("🚀 Compress", type="primary", use_container_width=True):
            with st.spinner(f"Compressing with {method}..."):
                start_time = time.time()
                
                try:
                    # Get compressor
                    if method == 'auto':
                        # Auto-detect best method
                        entropy = calculate_entropy(original_image)
                        unique_vals = len(np.unique(original_image))
                        
                        if unique_vals < 32:
                            method = 'rle'
                        elif entropy < 3.0:
                            method = 'differential'
                        else:
                            method = 'huffman'
                        
                        st.info(f"🤖 Auto-selected: {method.upper()}")
                    
                    compressor_class = COMPRESSORS[method]
                    
                    # Create compressor with parameters
                    if method == 'sparse':
                        compressor = compressor_class(sampling_rate=sampling_rate)
                    elif method == 'dct':
                        compressor = compressor_class(quality=quality)
                    else:
                        compressor = compressor_class()
                    
                    # Compress
                    compressed_bytes, metadata = compressor.compress(original_image)
                    
                    elapsed = time.time() - start_time
                    
                    # Get stats
                    stats = compressor.get_stats()
                    
                    # Store in session
                    st.session_state.encoded_data = {
                        'original': original_image,
                        'compressed_bytes': compressed_bytes,
                        'metadata': metadata,
                        'stats': stats,
                        'method': method,
                        'elapsed_time': elapsed,
                    }
                    
                    st.success(f"✅ Compression complete in {elapsed:.3f}s!")
                    
                except Exception as e:
                    st.error(f"❌ Compression failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
    else:
        st.info("👆 Upload or generate an image to begin")

# Results section
if st.session_state.encoded_data:
    st.markdown("---")
    st.header("📊 Compression Results")
    
    data = st.session_state.encoded_data
    stats = data['stats']
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        original_size = data['original'].size * 1  # 1 byte per pixel
        st.metric("Original Size", f"{original_size:,} bytes")
    
    with col2:
        compressed_size = len(data['compressed_bytes'])
        st.metric("Compressed Size", f"{compressed_size:,} bytes")
    
    with col3:
        ratio = stats.get('compression_ratio', 1.0)
        st.metric("Compression Ratio", f"{ratio:.2f}x")
    
    with col4:
        entropy = stats.get('entropy', 0)
        st.metric("Entropy", f"{entropy:.3f} bpp")
    
    # Detailed stats
    with st.expander("📈 Detailed Statistics"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Compression Metrics**")
            for key in ['method', 'compression_ratio', 'entropy', 'bits_per_pixel']:
                if key in stats:
                    st.text(f"{key}: {stats[key]}")
        
        with col2:
            st.markdown("**Performance**")
            st.text(f"Time: {data['elapsed_time']:.3f}s")
            st.text(f"Speed: {data['original'].size / data['elapsed_time']:.0f} pixels/s")
    
    # Build descriptive filename: {stem}_image_{method}[_{qualifier}].dat
    _stem = st.session_state.get('input_stem', 'encoded')
    _method = data['method']
    _qualifier = None
    if _method == 'dct':
        _qualifier = quality_qualifier(data['stats'].get('quality', 0.8))
    elif _method == 'sparse':
        _qualifier = sampling_rate_qualifier(data['stats'].get('sampling_rate', 4))
    _dat_filename = make_output_filename(_stem, "image", _method, "dat", qualifier=_qualifier)

    st.download_button(
        label="💾 Download Compressed Data",
        data=data['compressed_bytes'],
        file_name=_dat_filename,
        mime="application/octet-stream",
        use_container_width=True
    )
    
    # Next steps
    st.info("👉 Go to **Decode** page to reconstruct the image!")

# Information
with st.expander("ℹ️ About Compression Methods"):
    st.markdown("""
    ### Method Characteristics
    
    **Naive** - Baseline, no compression (1.0x)
    - Simple flattening
    - Perfect quality
    
    **RLE** - Run-Length Encoding (4-10x on blocks)
    - Best for: uniform regions
    - Lossless
    
    **Differential** - Encode differences (2-5x)
    - Best for: smooth gradients
    - Reduces entropy up to 95%
    - Lossless
    
    **Huffman** - Variable-length codes (1.5-3x)
    - Best for: general purpose
    - Approaches entropy limit
    - Lossless
    
    **Sparse** - Subsample + interpolate (10-50x)
    - Best for: quick preview
    - Lossy (interpolation)
    
    **DCT** - Frequency domain (5-20x)
    - Best for: natural photos
    - JPEG-style
    - Lossy (adjustable quality)
    """)
