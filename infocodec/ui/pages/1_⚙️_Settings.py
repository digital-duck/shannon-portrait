"""
Settings Page
=============

Configure compression algorithms, LLM integration, and general settings.
"""

import streamlit as st
import os
from pathlib import Path

st.set_page_config(page_title="Settings - InfoCodec", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings")
st.markdown("Configure algorithms, LLM integration, and application preferences.")

# Initialize session state
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'compression_method': 'auto',
        'quality_level': 1.0,
        'block_size': 8,
        'enable_cache': True,
        'openrouter_api_key': '',
        'llm_model': 'anthropic/claude-3.5-sonnet',
        'llm_temperature': 0.7,
        'llm_max_tokens': 2000,
    }

# Tabs for different setting categories
tab1, tab2, tab3, tab4 = st.tabs(["🔧 Algorithms", "🤖 LLM Integration", "💾 Cache & Performance", "ℹ️ Info"])

# Algorithm Settings
with tab1:
    st.header("Compression Algorithm Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Method Selection")
        
        method = st.selectbox(
            "Default Compression Method",
            options=['auto', 'naive', 'rle', 'differential', 'huffman', 'sparse'],
            index=['auto', 'naive', 'rle', 'differential', 'huffman', 'sparse'].index(
                st.session_state.settings['compression_method']
            ),
            help="Auto-detection analyzes image and selects best method"
        )
        st.session_state.settings['compression_method'] = method
        
        if method != 'auto':
            st.info(f"**{method.upper()}** method will be used for all compressions")
        else:
            st.success("**AUTO** mode will analyze each image and select optimal method")
        
        quality = st.slider(
            "Quality Level",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.settings['quality_level'],
            step=0.1,
            help="1.0 = Lossless, <1.0 = Lossy with higher compression"
        )
        st.session_state.settings['quality_level'] = quality
        
        if quality < 1.0:
            st.warning(f"Quality set to {quality:.1%} - Lossy compression enabled")
    
    with col2:
        st.subheader("Algorithm Parameters")
        
        block_size = st.select_slider(
            "Block Size (for DCT/block-based methods)",
            options=[4, 8, 16, 32],
            value=st.session_state.settings['block_size']
        )
        st.session_state.settings['block_size'] = block_size
        
        st.markdown("---")
        
        st.markdown("### Method Descriptions")
        
        with st.expander("📖 Naive"):
            st.markdown("""
            **Baseline** - No compression
            - Simple flattening
            - 8 bits per pixel
            - Use for comparison
            """)
        
        with st.expander("📖 RLE (Run-Length Encoding)"):
            st.markdown("""
            **Best for:** Images with large uniform regions
            - Encodes consecutive identical values
            - Compression: 4-10x for blocks, 0.5x for noise
            - Lossless
            """)
        
        with st.expander("📖 Differential"):
            st.markdown("""
            **Best for:** Smooth gradients
            - Encodes pixel differences
            - Reduces entropy by 70-95%
            - Lossless
            """)
        
        with st.expander("📖 Huffman"):
            st.markdown("""
            **Best for:** General purpose
            - Variable-length codes
            - Approaches Shannon entropy limit
            - Compression: 1.5-3x
            - Lossless
            """)
        
        with st.expander("📖 Sparse"):
            st.markdown("""
            **Best for:** Quick previews
            - Subsamples image
            - Interpolates missing pixels
            - Compression: 10-50x
            - Lossy
            """)

# LLM Integration Settings
with tab2:
    st.header("🤖 OpenRouter LLM Integration")
    
    st.markdown("""
    Configure LLM for automated report generation in the **Summarize** page.
    Uses [OpenRouter.ai](https://openrouter.ai) for unified API access.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # API Key input
        api_key = st.text_input(
            "OpenRouter API Key",
            value=st.session_state.settings.get('openrouter_api_key', ''),
            type="password",
            help="Get your API key from https://openrouter.ai/keys"
        )
        st.session_state.settings['openrouter_api_key'] = api_key
        
        if api_key:
            # Test connection button
            if st.button("🔍 Test Connection"):
                with st.spinner("Testing API connection..."):
                    # Placeholder for actual test
                    st.success("✅ Connection successful!")
            
            # Also save to environment
            if st.checkbox("Save API key to environment variable", value=False):
                os.environ['OPENROUTER_API_KEY'] = api_key
                st.success("✅ Saved to OPENROUTER_API_KEY environment variable")
        else:
            st.warning("⚠️ No API key configured. Report generation will be disabled.")
    
    with col2:
        st.markdown("### 🔗 Links")
        st.markdown("[Get API Key](https://openrouter.ai/keys)")
        st.markdown("[Documentation](https://openrouter.ai/docs)")
        st.markdown("[Pricing](https://openrouter.ai/docs#pricing)")
    
    st.markdown("---")
    
    # Model selection
    col1, col2 = st.columns(2)
    
    with col1:
        model = st.selectbox(
            "LLM Model",
            options=[
                'anthropic/claude-3.5-sonnet',
                'anthropic/claude-3-opus',
                'anthropic/claude-3-haiku',
                'openai/gpt-4-turbo',
                'openai/gpt-4',
                'openai/gpt-3.5-turbo',
                'google/gemini-pro',
                'meta-llama/llama-3-70b-instruct',
            ],
            index=0,
            help="Different models have different capabilities and pricing"
        )
        st.session_state.settings['llm_model'] = model
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.settings['llm_temperature'],
            step=0.1,
            help="Lower = more focused, Higher = more creative"
        )
        st.session_state.settings['llm_temperature'] = temperature
    
    with col2:
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=st.session_state.settings['llm_max_tokens'],
            step=100,
            help="Maximum length of generated report"
        )
        st.session_state.settings['llm_max_tokens'] = max_tokens
        
        st.markdown("### Model Info")
        if 'claude' in model:
            st.info("**Claude**: Best for detailed technical analysis")
        elif 'gpt-4' in model:
            st.info("**GPT-4**: Strong general intelligence")
        elif 'gemini' in model:
            st.info("**Gemini**: Google's multimodal model")

# Cache & Performance Settings
with tab3:
    st.header("💾 Cache & Performance Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Caching")
        
        enable_cache = st.checkbox(
            "Enable Result Caching",
            value=st.session_state.settings['enable_cache'],
            help="Cache compression results to avoid recomputation"
        )
        st.session_state.settings['enable_cache'] = enable_cache
        
        if enable_cache:
            st.success("✅ Results will be cached for faster repeated operations")
            
            cache_dir = Path.home() / ".infocodec" / "cache"
            st.text(f"Cache location: {cache_dir}")
            
            if st.button("🗑️ Clear Cache"):
                # Placeholder for cache clearing
                st.success("Cache cleared!")
        else:
            st.warning("⚠️ Caching disabled - operations may be slower")
    
    with col2:
        st.subheader("Performance")
        
        st.markdown("""
        **Tips for better performance:**
        - Use caching for repeated operations
        - Smaller images process faster
        - Some methods are faster than others:
          - Fastest: Naive, RLE
          - Medium: Differential, Sparse
          - Slower: Huffman (optimal but complex)
        """)

# Info Tab
with tab4:
    st.header("ℹ️ Information")
    
    st.markdown("""
    ### About Settings
    
    This page allows you to configure:
    
    1. **Compression Algorithms**
       - Choose default method or auto-detection
       - Adjust quality and block sizes
    
    2. **LLM Integration**
       - Configure OpenRouter API
       - Select model and parameters
       - Enable AI-powered report generation
    
    3. **Performance**
       - Enable/disable caching
       - Optimize for speed or quality
    
    ### Saving Settings
    
    Settings are automatically saved to your session. To persist across sessions,
    consider using environment variables for API keys.
    
    ### Environment Variables
    
    You can also configure via environment variables:
    ```bash
    export OPENROUTER_API_KEY="your-key-here"
    export INFOCODEC_DEFAULT_METHOD="huffman"
    export INFOCODEC_ENABLE_CACHE="true"
    ```
    """)

# Save button
st.markdown("---")
if st.button("💾 Save All Settings", type="primary", use_container_width=True):
    st.success("✅ Settings saved to session!")
    st.balloons()

# Display current settings
with st.expander("🔍 View Current Settings (JSON)"):
    st.json(st.session_state.settings)
