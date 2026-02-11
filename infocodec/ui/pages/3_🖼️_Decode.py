"""
Decode Page
===========

Reconstruct images from compressed data.
"""

import streamlit as st
import numpy as np
import time

from infocodec.core.reconstructors import RECONSTRUCTORS

st.set_page_config(page_title="Decode - InfoCodec", page_icon="🖼️", layout="wide")

st.title("🖼️ Decode (Reconstruct)")
st.markdown("Reconstruct images from compressed data.")

# Check if we have encoded data from Encode page
has_encoded_data = 'encoded_data' in st.session_state and st.session_state.encoded_data

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📦 Compressed Data")
    
    if has_encoded_data:
        # Use data from Encode page
        data = st.session_state.encoded_data
        
        st.success(f"✅ Using data from Encode page")
        
        st.metric("Method", data['method'].upper())
        st.metric("Compressed Size", f"{len(data['compressed_bytes']):,} bytes")
        st.metric("Original Shape", f"{data['original'].shape[0]}×{data['original'].shape[1]}")
        
        # Show original for reference
        st.subheader("Original Image (Reference)")
        st.image(data['original'], use_column_width=True, clamp=True)
        
        use_encoded_data = st.checkbox("Use this data", value=True)
    else:
        st.warning("⚠️ No compressed data found. Please go to **Encode** page first.")
        use_encoded_data = False
        
        # Alternative: upload compressed file
        st.markdown("---")
        st.subheader("Or Upload Compressed File")
        
        uploaded_file = st.file_uploader(
            "Choose a .dat file",
            type=['dat'],
            help="Upload a compressed .dat file from CLI or previous session"
        )
        
        if uploaded_file is not None:
            st.info("🚧 File upload reconstruction coming soon!")

with col2:
    st.header("🔄 Reconstruction")
    
    if has_encoded_data and use_encoded_data:
        data = st.session_state.encoded_data
        
        # Reconstruct button
        if st.button("🚀 Reconstruct", type="primary", use_container_width=True):
            with st.spinner("Reconstructing image..."):
                start_time = time.time()
                
                try:
                    # Get reconstructor
                    method = data['method']
                    reconstructor_class = RECONSTRUCTORS.get(method)
                    
                    if not reconstructor_class:
                        st.error(f"❌ No reconstructor found for method: {method}")
                    else:
                        reconstructor = reconstructor_class()
                        
                        # Reconstruct
                        reconstructed = reconstructor.reconstruct(
                            data['compressed_bytes'],
                            data['metadata']
                        )
                        
                        elapsed = time.time() - start_time
                        
                        # Store result
                        st.session_state.reconstructed_data = {
                            'image': reconstructed,
                            'method': method,
                            'elapsed_time': elapsed,
                            'stats': reconstructor.get_stats(),
                        }
                        
                        st.success(f"✅ Reconstruction complete in {elapsed:.3f}s!")
                        
                except Exception as e:
                    st.error(f"❌ Reconstruction failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Show reconstructed image
        if 'reconstructed_data' in st.session_state:
            recon_data = st.session_state.reconstructed_data
            
            st.subheader("Reconstructed Image")
            st.image(recon_data['image'], use_column_width=True, clamp=True)
            
            # Stats
            with st.expander("📊 Reconstruction Stats"):
                st.json(recon_data['stats'])
            
            # Quality comparison
            st.markdown("---")
            st.subheader("📈 Quality Metrics")
            
            from infocodec.core.metrics import calculate_psnr, calculate_ssim, calculate_mse
            
            original = data['original']
            reconstructed = recon_data['image']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                psnr = calculate_psnr(original, reconstructed)
                st.metric("PSNR", f"{psnr:.2f} dB" if psnr != float('inf') else "∞ (Perfect)")
            
            with col2:
                ssim = calculate_ssim(original, reconstructed)
                st.metric("SSIM", f"{ssim:.4f}")
            
            with col3:
                mse = calculate_mse(original, reconstructed)
                st.metric("MSE", f"{mse:.2f}")
            
            # Quality interpretation
            if psnr == float('inf'):
                st.success("🎯 **Perfect Reconstruction** - Lossless compression!")
            elif psnr > 40:
                st.success(f"✅ **Excellent Quality** - PSNR > 40 dB")
            elif psnr > 30:
                st.info(f"👍 **Good Quality** - PSNR 30-40 dB")
            elif psnr > 20:
                st.warning(f"⚠️ **Acceptable Quality** - PSNR 20-30 dB")
            else:
                st.error(f"❌ **Poor Quality** - PSNR < 20 dB")
            
            # Side-by-side comparison
            st.markdown("---")
            st.subheader("🔍 Side-by-Side Comparison")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Original**")
                st.image(original, use_column_width=True, clamp=True)
            
            with col2:
                st.markdown("**Reconstructed**")
                st.image(reconstructed, use_column_width=True, clamp=True)
            
            with col3:
                st.markdown("**Difference (Amplified)**")
                diff = np.abs(original.astype(int) - reconstructed.astype(int))
                diff_amplified = np.clip(diff * 10, 0, 255).astype(np.uint8)
                st.image(diff_amplified, use_column_width=True, clamp=True)
            
            # Next steps
            st.info("👉 Go to **Diff** page for detailed analysis!")
    
    else:
        st.info("👆 Use compressed data from Encode page or upload a file")

# Information
with st.expander("ℹ️ About Reconstruction"):
    st.markdown("""
    ### Reconstruction Process
    
    1. **Read Metadata** - Extract compression method and parameters
    2. **Select Reconstructor** - Choose appropriate decoder
    3. **Decode** - Apply inverse of compression algorithm
    4. **Validate** - Check quality metrics
    
    ### Quality Metrics
    
    **PSNR (Peak Signal-to-Noise Ratio)**
    - > 40 dB: Excellent
    - 30-40 dB: Good
    - 20-30 dB: Acceptable  
    - < 20 dB: Poor
    - ∞: Perfect (lossless)
    
    **SSIM (Structural Similarity Index)**
    - 0.0 - 1.0 scale
    - > 0.95: Very similar
    - > 0.90: Similar
    - < 0.90: Noticeable differences
    
    **MSE (Mean Squared Error)**
    - Lower is better
    - 0 = perfect match
    """)
