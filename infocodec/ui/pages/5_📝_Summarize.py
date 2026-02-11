"""
Summarize Page
==============

Generate AI-powered analysis reports of compression experiments using OpenRouter.
"""

import streamlit as st

from infocodec.core.metrics import comprehensive_quality_analysis
from infocodec.utils.openrouter import get_client, get_api_key, OpenRouterKeyError
from infocodec.utils.paths import make_output_filename

st.set_page_config(page_title="Summarize - InfoCodec", page_icon="📝", layout="wide")

st.title("📝 Summarize")
st.markdown("Generate an AI-powered analysis report of your compression experiment.")

# ── Prerequisites check ────────────────────────────────────────────────────────
has_encoded = 'encoded_data' in st.session_state and st.session_state.encoded_data
has_decoded = 'reconstructed_data' in st.session_state and st.session_state.reconstructed_data

if not has_encoded or not has_decoded:
    st.warning("⚠️ No experiment data found. Complete **Encode** and **Decode** first.")
    st.info("👉 🗜️ Encode → 🖼️ Decode → 📊 Diff → here")
    st.stop()

# ── Resolve API key ────────────────────────────────────────────────────────────
settings = st.session_state.get('settings', {})
api_key = settings.get('openrouter_api_key', '')

if not api_key:
    try:
        api_key = get_api_key()
    except OpenRouterKeyError:
        pass

if not api_key:
    st.error(
        "❌ OpenRouter API key not configured. "
        "Go to **⚙️ Settings → LLM Integration** to add one."
    )
    st.stop()

# ── Gather experiment data ─────────────────────────────────────────────────────
original = st.session_state.encoded_data['original']
reconstructed = st.session_state.reconstructed_data['image']
method = st.session_state.encoded_data['method']
compressed_size = len(st.session_state.encoded_data['compressed_bytes'])

analysis = comprehensive_quality_analysis(
    original=original,
    reconstructed=reconstructed,
    original_size=original.size,
    compressed_size=compressed_size,
)

psnr = analysis['psnr_db']
psnr_str = "∞ (perfect, lossless)" if psnr == float('inf') else f"{psnr:.2f} dB"
modality = "color RGB" if original.ndim == 3 else "grayscale"

# ── Experiment summary banner ──────────────────────────────────────────────────
st.header("📊 Experiment at a Glance")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Method", method.upper())
with col2:
    st.metric("PSNR", "∞ dB" if psnr == float('inf') else f"{psnr:.2f} dB")
with col3:
    st.metric("SSIM", f"{analysis['ssim']:.4f}")
with col4:
    st.metric("Ratio", f"{analysis['compression_ratio']:.2f}x")
with col5:
    st.metric("Efficiency", f"{analysis['efficiency_percent']:.1f}%")

# ── Report configuration ───────────────────────────────────────────────────────
st.markdown("---")
st.subheader("⚙️ Report Configuration")

col1, col2 = st.columns([1, 2])

with col1:
    report_style = st.selectbox(
        "Report Style",
        options=["Technical", "Educational", "Executive Summary"],
        help="Shapes the tone and depth of the generated report",
    )
    extra_context = st.text_area(
        "Additional Context (optional)",
        placeholder="E.g., 'This is a medical X-ray image' or 'Focus on the rate-distortion trade-off'",
        height=100,
    )

with col2:
    llm_model = settings.get('llm_model', 'anthropic/claude-3.5-sonnet')
    llm_temperature = settings.get('llm_temperature', 0.7)
    llm_max_tokens = settings.get('llm_max_tokens', 2000)

    st.markdown(f"**Model:** `{llm_model}`")
    st.markdown(f"**Temperature:** {llm_temperature} &nbsp; **Max tokens:** {llm_max_tokens}")
    st.caption("Change these in ⚙️ Settings → LLM Integration")

# ── Build prompt ───────────────────────────────────────────────────────────────
_style_instructions = {
    "Technical": (
        "Write a detailed technical analysis suitable for a research paper or engineering report. "
        "Use precise terminology, cite the metrics explicitly, and discuss theoretical implications."
    ),
    "Educational": (
        "Write a clear educational explanation suitable for students learning about information theory. "
        "Define key concepts, explain intuitions, and connect results to Shannon's foundational ideas."
    ),
    "Executive Summary": (
        "Write a concise executive summary (bullet points where appropriate) focused on key findings, "
        "practical implications, and actionable recommendations. Avoid excessive jargon."
    ),
}

_default_prompt = f"""\
{_style_instructions[report_style]}

Analyse this image compression experiment conducted with InfoCodec, a tool for \
exploring Shannon's Information Theory.

## Experiment Details
- Compression Method : {method.upper()}
- Image Shape        : {original.shape[0]}×{original.shape[1]} pixels ({modality})
- Total Pixels       : {analysis['num_pixels']:,}

## Information Theory Metrics
- Original Entropy      : {analysis['original_entropy']:.3f} bits/symbol
- Reconstructed Entropy : {analysis['reconstructed_entropy']:.3f} bits/symbol
- Entropy Reduction     : {analysis['entropy_reduction']:.1f}%
- Theoretical Min Bits  : {analysis['theoretical_min_bits']:,.0f} bits
- Coding Efficiency     : {analysis['efficiency_percent']:.1f}%  (how close to Shannon limit)

## Quality Metrics
- PSNR : {psnr_str}
- SSIM : {analysis['ssim']:.4f}   (1.0 = identical)
- MSE  : {analysis['mse']:.2f}

## Compression Metrics
- Original Size     : {analysis['original_size_bytes']:,} bytes ({analysis['original_bpp']:.0f} bpp)
- Compressed Size   : {analysis['compressed_size_bytes']:,} bytes ({analysis['bits_per_pixel']:.2f} bpp)
- Compression Ratio : {analysis['compression_ratio']:.2f}×
- Space Saved       : {analysis['space_saved_percent']:.1f}%
{f"{chr(10)}## Additional Context{chr(10)}{extra_context}" if extra_context.strip() else ""}

Please structure your report with sections covering:
1. Image characteristics and entropy interpretation
2. How {method.upper()} works and why it achieves this compression ratio
3. Quality assessment — what PSNR and SSIM values mean in practice
4. Proximity to Shannon's theoretical limit and coding efficiency
5. Trade-offs and recommendations for this type of image/use case
"""

st.markdown("---")
st.subheader("📋 Prompt")
prompt = st.text_area(
    "Review and edit before generating:",
    value=_default_prompt,
    height=320,
)

# ── Generate ───────────────────────────────────────────────────────────────────
if st.button("🤖 Generate Report", type="primary", use_container_width=True):
    with st.spinner(f"Generating report with {llm_model} …"):
        try:
            client = get_client(api_key=api_key)
            response = client.chat.completions.create(
                model=llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert in information theory, data compression, and "
                            "signal processing. Provide precise, insightful analysis grounded "
                            "in Claude Shannon's foundational work."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=llm_temperature,
                max_tokens=llm_max_tokens,
            )
            st.session_state['summary_report'] = response.choices[0].message.content
            st.session_state['summary_method'] = method
        except Exception as exc:
            st.error(f"❌ Report generation failed: {exc}")
            import traceback
            st.code(traceback.format_exc())

# ── Display and download ───────────────────────────────────────────────────────
if 'summary_report' in st.session_state:
    st.markdown("---")
    st.subheader("📄 Generated Report")
    st.markdown(st.session_state['summary_report'])

    st.markdown("---")
    _stem = st.session_state.get('input_stem', 'encoded')
    _saved_method = st.session_state.get('summary_method', method)
    _filename_md = make_output_filename(_stem, "image", _saved_method, "md", prefix="summary")
    _filename_txt = make_output_filename(_stem, "image", _saved_method, "txt", prefix="summary")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="💾 Download Report (Markdown)",
            data=st.session_state['summary_report'],
            file_name=_filename_md,
            mime="text/markdown",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            label="💾 Download Report (Plain Text)",
            data=st.session_state['summary_report'],
            file_name=_filename_txt,
            mime="text/plain",
            use_container_width=True,
        )
