"""
Diff Page
=========

Detailed analysis of compression quality and information loss.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from infocodec.core.metrics import (
    comprehensive_quality_analysis,
    format_metrics_report,
    analyze_data_distribution
)

st.set_page_config(page_title="Diff - InfoCodec", page_icon="📊", layout="wide")

st.title("📊 Diff Analysis")
st.markdown("Quantify and visualize information loss from compression.")

# Check for data
has_data = (
    'encoded_data' in st.session_state and 
    'reconstructed_data' in st.session_state and
    st.session_state.encoded_data and
    st.session_state.reconstructed_data
)

if not has_data:
    st.warning("⚠️ No data available. Please complete **Encode** and **Decode** steps first.")
    st.info("👉 Go to **Encode** page → Compress an image → **Decode** page → Reconstruct")
    st.stop()

# Get data
original = st.session_state.encoded_data['original']
reconstructed = st.session_state.reconstructed_data['image']
method = st.session_state.encoded_data['method']
compressed_size = len(st.session_state.encoded_data['compressed_bytes'])

# Comprehensive analysis
analysis = comprehensive_quality_analysis(
    original=original,
    reconstructed=reconstructed,
    original_size=original.size,
    compressed_size=compressed_size
)

# Top metrics
st.header("🎯 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Compression Ratio", f"{analysis['compression_ratio']:.2f}x")

with col2:
    psnr = analysis['psnr_db']
    delta = "∞" if psnr == float('inf') else f"{psnr:.1f}"
    st.metric("PSNR", f"{delta} dB")

with col3:
    st.metric("SSIM", f"{analysis['ssim']:.4f}")

with col4:
    st.metric("Space Saved", f"{analysis['space_saved_percent']:.1f}%")

with col5:
    st.metric("Efficiency", f"{analysis['efficiency_percent']:.1f}%")

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["📈 Visual Analysis", "📊 Statistical Analysis", "🔬 Information Theory", "📝 Report"])

with tab1:
    st.subheader("Visual Comparison")
    
    # Side-by-side images
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Original**")
        st.image(original, use_container_width=True, clamp=True)
        st.caption(f"Size: {original.shape[0]}×{original.shape[1]}")
    
    with col2:
        st.markdown("**Reconstructed**")
        st.image(reconstructed, use_container_width=True, clamp=True)
        st.caption(f"Method: {method.upper()}")
    
    with col3:
        st.markdown("**Absolute Difference**")
        diff = np.abs(original.astype(int) - reconstructed.astype(int)).astype(np.uint8)
        st.image(diff, use_container_width=True, clamp=True)
        st.caption(f"Max error: {np.max(diff)}")
    
    # Difference heatmap
    st.markdown("---")
    st.subheader("Error Heatmap")
    
    fig = px.imshow(diff, color_continuous_scale='hot', 
                    labels={'color': 'Error'},
                    title=f"Pixel-wise Error Distribution (Max: {np.max(diff)})")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Error histogram
    st.subheader("Error Distribution")
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=diff.flatten(), nbinsx=50, name='Error'))
    fig.update_layout(
        title="Histogram of Pixel Errors",
        xaxis_title="Error Magnitude",
        yaxis_title="Frequency",
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Statistical Analysis")
    
    # Distribution comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Distribution**")
        orig_dist = analyze_data_distribution(original)
        st.json(orig_dist)
    
    with col2:
        st.markdown("**Reconstructed Distribution**")
        recon_dist = analyze_data_distribution(reconstructed)
        st.json(recon_dist)
    
    # Histograms
    st.markdown("---")
    st.subheader("Pixel Value Distributions")
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=original.flatten(), nbinsx=50, 
                               name='Original', opacity=0.7))
    fig.add_trace(go.Histogram(x=reconstructed.flatten(), nbinsx=50,
                               name='Reconstructed', opacity=0.7))
    fig.update_layout(
        title="Pixel Value Distributions",
        xaxis_title="Pixel Value",
        yaxis_title="Frequency",
        barmode='overlay'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 2D scatter comparison
    st.subheader("Pixel-by-Pixel Correlation")
    
    # Sample pixels for scatter plot (all pixels for small images)
    if original.size < 10000:
        sample_orig = original.flatten()
        sample_recon = reconstructed.flatten()
    else:
        indices = np.random.choice(original.size, size=10000, replace=False)
        sample_orig = original.flatten()[indices]
        sample_recon = reconstructed.flatten()[indices]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sample_orig,
        y=sample_recon,
        mode='markers',
        marker=dict(size=3, opacity=0.5),
        name='Pixels'
    ))
    fig.add_trace(go.Scatter(
        x=[0, 255],
        y=[0, 255],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Perfect match'
    ))
    fig.update_layout(
        title="Original vs Reconstructed Pixel Values",
        xaxis_title="Original",
        yaxis_title="Reconstructed",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Information Theory Analysis")
    
    # Shannon metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📐 Entropy Analysis")
        st.metric("Original Entropy", f"{analysis['original_entropy']:.3f} bits/symbol")
        st.metric("Reconstructed Entropy", f"{analysis['reconstructed_entropy']:.3f} bits/symbol")
        st.metric("Entropy Reduction", f"{analysis['entropy_reduction']:.1f}%")
        
        st.markdown("""
        **Interpretation:**
        - Lower entropy = more predictable
        - Entropy sets compression limit
        - Can't compress below entropy (losslessly)
        """)
    
    with col2:
        st.markdown("### 💾 Compression Analysis")
        st.metric("Original BPP", f"{analysis['original_bpp']:.2f}")
        st.metric("Compressed BPP", f"{analysis['bits_per_pixel']:.2f}")
        st.metric("Compression Ratio", f"{analysis['compression_ratio']:.2f}x")
        
        st.markdown("""
        **BPP = Bits Per Pixel:**
        - Original: 8 BPP (standard)
        - Compressed: varies by method
        - Lower BPP = better compression
        """)
    
    # Theoretical limits
    st.markdown("---")
    st.markdown("### 🎯 Shannon's Theoretical Limits")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Theoretical Minimum", f"{analysis['theoretical_min_bits']:,.0f} bits")
        st.caption("H(X) × num_pixels")
    
    with col2:
        st.metric("Actual Compressed", f"{analysis['compressed_size_bytes'] * 8:,.0f} bits")
        st.caption("Achieved in practice")
    
    with col3:
        st.metric("Efficiency", f"{analysis['efficiency_percent']:.1f}%")
        st.caption("How close to theoretical")
    
    # Efficiency interpretation
    efficiency = analysis['efficiency_percent']
    if efficiency > 95:
        st.success("✅ **Excellent!** Near-optimal compression (>95% efficiency)")
    elif efficiency > 80:
        st.info("👍 **Good** compression efficiency (80-95%)")
    elif efficiency > 60:
        st.warning("⚠️ **Moderate** efficiency (60-80%) - room for improvement")
    else:
        st.error("❌ **Low** efficiency (<60%) - significant overhead")
    
    # Rate-distortion
    st.markdown("---")
    st.markdown("### 📉 Rate-Distortion Trade-off")
    
    st.markdown(f"""
    **Current Operating Point:**
    - Rate: {analysis['bits_per_pixel']:.2f} bits/pixel
    - Distortion: MSE = {analysis['mse']:.2f}
    - PSNR: {analysis['psnr_db']:.2f} dB
    
    **Interpretation:**
    - Lower rate → more compression → higher distortion
    - Higher rate → less compression → lower distortion
    - Optimal point depends on application
    """)

with tab4:
    st.subheader("📝 Comprehensive Report")
    
    # Formatted report
    report = format_metrics_report(analysis)
    st.code(report, language='text')
    
    # Download options
    col1, col2 = st.columns(2)
    
    with col1:
        # Download as text
        st.download_button(
            label="💾 Download Report (TXT)",
            data=report,
            file_name=f"compression_report_{method}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # Download as JSON
        import json
        json_report = json.dumps(analysis, indent=2)
        st.download_button(
            label="💾 Download Metrics (JSON)",
            data=json_report,
            file_name=f"compression_metrics_{method}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Next steps
    st.info("👉 Go to **Summarize** page to generate AI-powered analysis!")

# Footer with method info
st.markdown("---")
st.markdown(f"**Method:** {method.upper()} • **Shape:** {original.shape[0]}×{original.shape[1]} • **Size:** {original.size:,} pixels")
