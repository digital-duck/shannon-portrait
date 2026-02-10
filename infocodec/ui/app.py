"""
InfoCodec Streamlit UI
======================

Interactive web interface for exploring Shannon's Information Theory
through image compression and reconstruction.
"""

import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="InfoCodec - Shannon Portrait",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-style: italic;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Main page content
def main():
    # Header
    st.markdown('<h1 class="main-header">InfoCodec</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Information Coding & Encoding • Exploring Shannon\'s Information Theory</p>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x200.png?text=Shannon+Portrait", 
                use_container_width=True)
        st.markdown("### Navigation")
        st.markdown("""
        Use the pages in the sidebar to:
        - **⚙️ Settings**: Configure algorithms and LLM
        - **📤 Encode**: Compress your data  
        - **📥 Decode**: Reconstruct from compressed
        - **📊 Diff**: Analyze quality loss
        - **📝 Summarize**: Generate AI report
        """)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This tool demonstrates **Claude Shannon's Information Theory** 
        through practical compression experiments.
        
        **Key Concepts:**
        - Shannon Entropy
        - Channel Capacity
        - Lossy vs Lossless
        - Rate-Distortion
        """)
    
    # Main content
    st.markdown("## Welcome to InfoCodec!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 What is This?")
        st.markdown("""
        InfoCodec is a research and educational tool for exploring 
        **information theory** through practical experiments.
        
        **Use Cases:**
        - Research information representation
        - Educational demonstrations
        - Compression algorithm comparison
        - Shannon theory visualization
        """)
        
        st.markdown("### 🚀 Quick Start")
        st.markdown("""
        1. Go to **Settings** to configure
        2. Upload an image in **Encode**
        3. Try different compression methods
        4. View results in **Decode** and **Diff**
        5. Generate report in **Summarize**
        """)
    
    with col2:
        st.markdown("### 📊 Supported Methods")
        
        methods = [
            ("Naive", "Baseline - no compression", "1.0x"),
            ("RLE", "Run-Length Encoding", "4-10x"),
            ("Differential", "Encode differences", "2-5x"),
            ("Huffman", "Variable-length codes", "1.5-3x"),
            ("Sparse", "Subsample & interpolate", "10-50x"),
        ]
        
        for name, desc, ratio in methods:
            st.markdown(f"**{name}** • {desc} • *{ratio}*")
    
    # Information Theory refresher
    with st.expander("📚 Shannon's Information Theory - Quick Refresher"):
        st.markdown("""
        ### Entropy
        ```
        H(X) = -Σ p(x) log₂(p(x))
        ```
        Measures information content. Lower entropy → more predictable → better compression.
        
        ### Channel Capacity
        ```
        C = B log₂(1 + SNR)
        ```
        Maximum rate of reliable communication. Fundamental limit.
        
        ### Rate-Distortion
        Trade-off between compression (rate) and quality (distortion).
        More compression → more quality loss.
        """)
    
    # Example workflow
    st.markdown("## 🎨 Example Workflow")
    
    tab1, tab2, tab3 = st.tabs(["📷 Image", "🎵 Audio (Coming Soon)", "📝 Text (Coming Soon)"])
    
    with tab1:
        st.markdown("""
        ### Image Compression Workflow
        
        1. **Upload**: Load Shannon's portrait or your own image
        2. **Analyze**: View entropy and distribution
        3. **Compress**: Select method (auto or manual)
        4. **Transmit**: Simulate 1D wire transmission
        5. **Reconstruct**: Decode at receiver
        6. **Compare**: Measure PSNR, SSIM, compression ratio
        
        **Try different methods** to see how they perform on different image types!
        """)
    
    with tab2:
        st.info("🎵 Audio compression coming in future release")
    
    with tab3:
        st.info("📝 Text compression coming in future release")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888;'>
        Built with ❤️ for exploring Shannon's Information Theory<br>
        <em>"The fundamental problem of communication is that of reproducing at one point 
        exactly or approximately a message selected at another." — Claude Shannon</em>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
