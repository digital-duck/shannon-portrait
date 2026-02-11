"""
Explain Page
============

Educational reference for all algorithms and concepts used in InfoCodec.
"""

import streamlit as st

st.set_page_config(page_title="Explain - InfoCodec", page_icon="🎓", layout="wide")

st.title("🎓 Explain")
st.markdown("A guided tour of Shannon's Information Theory and every algorithm used in this app.")

# ── Navigation helper ──────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📡 Information Theory",
    "🔒 Lossless Algorithms",
    "✂️ Lossy Algorithms",
    "📐 Quality Metrics",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Information Theory Foundations
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("📡 Shannon's Information Theory")

    st.markdown("""
    Claude Shannon's 1948 paper *"A Mathematical Theory of Communication"* created the
    entire field of information theory. Three ideas underpin everything in this app.
    """)

    # ── Entropy ───────────────────────────────────────────────────────────────
    with st.expander("🎲 Shannon Entropy — H(X)", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it is:** The average amount of *surprise* (information) per symbol in a source.

            **Formula:**
            ```
            H(X) = -Σ p(x) · log₂(p(x))    (bits per symbol)
            ```

            **Intuition:**
            - A fair coin flip: H = 1 bit (maximum uncertainty)
            - A biased coin (99% heads): H ≈ 0.08 bits (very predictable)
            - A uniform 256-value image: H = 8 bits/pixel (maximally random)
            - A smooth gradient image: H ≈ 3–5 bits/pixel (very compressible)

            **Why it matters for compression:**
            Entropy is the *theoretical lower bound* on how many bits per symbol any
            lossless compressor can achieve. You cannot compress below entropy without
            losing information.

            **In this app:** Shown on the Encode page and used to calculate Coding Efficiency
            on the Diff page.
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Entropy (information theory)](https://en.wikipedia.org/wiki/Entropy_(information_theory))")
            st.markdown("[YouTube — Search: Shannon entropy explained](https://www.youtube.com/results?search_query=shannon+entropy+information+theory+explained)")
            st.markdown("[YouTube — 3Blue1Brown: Wordle & information](https://www.youtube.com/results?search_query=3blue1brown+information+theory+wordle)")

    # ── Source Coding Theorem ──────────────────────────────────────────────────
    with st.expander("📜 Shannon's Source Coding Theorem"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it says:** It is possible to compress a source to an average code length
            arbitrarily close to its entropy H(X), but no further (losslessly).

            **Formally:**
            ```
            H(X) ≤ L < H(X) + 1      where L = average code length
            ```

            **Practical meaning:**
            - Huffman coding approaches the entropy limit within 1 bit per symbol
            - Arithmetic coding can get within 0.001 bits
            - No lossless code can beat H(X)

            **Coding Efficiency** (shown on the Diff page):
            ```
            Efficiency = (H(X) × N) / (compressed bits) × 100%
            ```
            where N is the number of pixels. Values above 95% are excellent.
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Shannon's source coding theorem](https://en.wikipedia.org/wiki/Shannon%27s_source_coding_theorem)")
            st.markdown("[YouTube — Search: source coding theorem](https://www.youtube.com/results?search_query=shannon+source+coding+theorem+compression)")

    # ── Channel Capacity ───────────────────────────────────────────────────────
    with st.expander("📶 Channel Capacity — C"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it is:** The maximum rate at which information can be reliably transmitted
            over a noisy channel.

            **Shannon-Hartley formula:**
            ```
            C = B · log₂(1 + S/N)    (bits per second)
            ```
            where B = bandwidth (Hz), S/N = signal-to-noise ratio.

            **Intuition:** A wider pipe (B) or less noise (high S/N) → more capacity.
            This is why fibre optic cables with low noise carry so much data.

            **Connection to PSNR:** PSNR is essentially a measurement of S/N after
            compression. High PSNR = low distortion = the reconstructed image is a
            faithful copy of what was "transmitted" through the compression channel.
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Channel capacity](https://en.wikipedia.org/wiki/Channel_capacity)")
            st.markdown("[Wikipedia — Shannon–Hartley theorem](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem)")
            st.markdown("[YouTube — Search: channel capacity Shannon](https://www.youtube.com/results?search_query=channel+capacity+shannon+hartley+explained)")

    # ── Rate–Distortion ────────────────────────────────────────────────────────
    with st.expander("📉 Rate–Distortion Theory"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it is:** The fundamental trade-off between how many bits you use (rate)
            and how much quality you lose (distortion).

            **Key insight:**
            - For *lossless* compression, rate ≥ H(X) — you can never go below entropy
            - For *lossy* compression, you can go below H(X) by accepting distortion
            - The rate-distortion function R(D) gives the minimum rate needed to achieve
              distortion D

            **In practice:**
            | Method | Rate | Distortion |
            |--------|------|------------|
            | Naive  | 8 bpp | 0 |
            | Huffman | ~H(X) bpp | 0 |
            | DCT (quality=1.0) | ~2–4 bpp | low |
            | DCT (quality=0.1) | ~0.5 bpp | high |
            | Sparse (rate=4) | ~0.5 bpp | medium |

            **Shown on the Diff page** under "Rate–Distortion Trade-off".
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Rate–distortion theory](https://en.wikipedia.org/wiki/Rate%E2%80%93distortion_theory)")
            st.markdown("[YouTube — Search: rate distortion theory explained](https://www.youtube.com/results?search_query=rate+distortion+theory+compression)")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Lossless Algorithms
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("🔒 Lossless Compression Algorithms")
    st.markdown("""
    Lossless algorithms reconstruct the image *exactly*. After decode, PSNR = ∞ and SSIM = 1.0000.
    The trade-off is that you are bounded by Shannon entropy — you cannot compress below H(X).
    """)

    # ── Naive ──────────────────────────────────────────────────────────────────
    with st.expander("⬜ Naive — Baseline (1.0×)", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it does:** No compression at all — just flattens the 2D pixel array
            into a 1D byte stream. Used as a *baseline* to compare all other methods.

            **How it works:**
            ```
            image (H×W) → flatten → bytes [p0, p1, p2, ...]
            ```

            **Steps:**
            1. Cast pixels to `uint8`
            2. Call `array.tobytes()` — the "compressed" stream IS the raw pixels
            3. Store shape in metadata for reconstruction

            **When to use:** Never for real compression. Useful as a reference point —
            any other method should do better on compressible images.

            **Compression ratio:** Always 1.0× (no change in size)
            **Quality:** Perfect (PSNR = ∞)
            **Type:** Lossless
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Lossless compression](https://en.wikipedia.org/wiki/Lossless_compression)")

    # ── RLE ────────────────────────────────────────────────────────────────────
    with st.expander("▬▬▬ RLE — Run-Length Encoding (4–10×)"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it does:** Replaces consecutive identical values with a (value, count) pair.

            **Example:**
            ```
            Raw pixels:  [255, 255, 255, 255, 0, 0, 128, 128, 128]
            RLE encoded: [(255,4), (0,2), (128,3)]
            Bytes saved: 9 → 6  (2 bytes per pair vs 1 byte per pixel for runs ≥ 2)
            ```

            **How it works in this app:**
            ```python
            current_val, count = flat_data[0], 1
            for val in flat_data[1:]:
                if val == current_val and count < 255:
                    count += 1
                else:
                    emit(current_val, count)
                    current_val, count = val, 1
            emit(current_val, count)   # flush last run
            ```

            **When it wins:** Images with large uniform regions — logos, diagrams,
            pixel art, screenshots with solid backgrounds.

            **When it loses:** Noisy or photographic images — every pixel differs,
            so every run has length 1 → output is *2× larger* than input.

            **Compression ratio:** 4–10× on block patterns; < 1× on noise
            **Quality:** Perfect (lossless)
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Run-length encoding](https://en.wikipedia.org/wiki/Run-length_encoding)")
            st.markdown("[YouTube — Search: run length encoding](https://www.youtube.com/results?search_query=run+length+encoding+compression+explained)")

    # ── Differential ──────────────────────────────────────────────────────────
    with st.expander("📈 Differential — Delta Encoding (2–5×)"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it does:** Instead of storing absolute pixel values, stores the
            *difference* between consecutive pixels (delta encoding).

            **Example:**
            ```
            Raw pixels:   [100, 102, 105, 104, 103]
            Differences:  [100,  +2,  +3,  -1,  -1]   ← much smaller values!
            Entropy of differences << Entropy of raw pixels
            ```

            **How it works:**
            ```
            Encode:  diff[0] = pixel[0]
                     diff[i] = pixel[i] - pixel[i-1]   (stored as int16)

            Decode:  pixel = cumsum(diff)               (cumulative sum)
            ```

            **Why it reduces entropy:** In a smooth image, neighbouring pixels are
            similar — differences cluster tightly around 0, making the distribution
            much more predictable (lower entropy) than the raw values.

            **Entropy reduction** (shown in Diff page) can be 70–95% on gradients.

            **When it wins:** Smooth gradients, natural photographs, time-series data.
            **When it loses:** High-frequency noise — differences are as large as the values.

            **Compression ratio:** 2–5× on smooth images
            **Quality:** Perfect (lossless)
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Delta encoding](https://en.wikipedia.org/wiki/Delta_encoding)")
            st.markdown("[Wikipedia — Predictive coding](https://en.wikipedia.org/wiki/Predictive_coding)")
            st.markdown("[YouTube — Search: delta encoding differential compression](https://www.youtube.com/results?search_query=delta+encoding+differential+compression+tutorial)")

    # ── Huffman ────────────────────────────────────────────────────────────────
    with st.expander("🌲 Huffman Coding — Variable-Length Codes (1.5–3×)"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it does:** Assigns shorter bit codes to frequent symbols and longer
            codes to rare symbols — optimally exploiting the probability distribution.

            **Example (frequency-ordered):**
            ```
            Symbol | Frequency | Fixed (8 bits) | Huffman code
            -------|-----------|----------------|-------------
               200 |     40%   |   11001000     |     0       (1 bit)
               128 |     30%   |   10000000     |    10       (2 bits)
                50 |     20%   |   00110010     |   110       (3 bits)
                 0 |     10%   |   00000000     |   111       (3 bits)
            Average: 0.4×1 + 0.3×2 + 0.2×3 + 0.1×3 = 1.9 bits  vs  8 bits fixed
            ```

            **How the tree is built (greedy algorithm):**
            ```
            1. Create one leaf node per unique symbol, weighted by frequency
            2. Repeat until one tree remains:
               a. Pop the two lowest-frequency nodes
               b. Merge into a parent node (sum of frequencies)
               c. Push parent back into the priority queue
            3. Assign 0 to left branches, 1 to right branches
            4. Each leaf's path from root = its codeword
            ```

            **Shannon's guarantee:** Huffman achieves H(X) ≤ L < H(X) + 1 bits/symbol.
            In practice this app reaches **97–99% coding efficiency**.

            **In this app:** The code table is serialised into the `.dat` file header
            alongside the compressed bitstream, enabling self-contained decoding.

            **Compression ratio:** 1.5–3× for typical images
            **Quality:** Perfect (lossless)
            **Efficiency:** 97–99% of Shannon limit
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)")
            st.markdown("[YouTube — Search: Huffman coding tree algorithm](https://www.youtube.com/results?search_query=huffman+coding+tree+algorithm+explained)")
            st.markdown("[YouTube — Computerphile: Huffman](https://www.youtube.com/results?search_query=computerphile+huffman+encoding)")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Lossy Algorithms
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("✂️ Lossy Compression Algorithms")
    st.markdown("""
    Lossy algorithms trade quality for much higher compression ratios. They deliberately
    discard information that is hard to perceive — the decoded image is an *approximation*
    of the original. PSNR and SSIM measure how much quality is lost.
    """)

    # ── Sparse ─────────────────────────────────────────────────────────────────
    with st.expander("🎯 Sparse Sampling — Subsample & Interpolate (10–50×)", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it does:** Keeps only every N-th pixel (spatial subsampling) and
            reconstructs the missing pixels by interpolation.

            **How it works:**
            ```
            Encode:
              for row in range(0, H, N):
                for col in range(0, W, N):
                  store (row, col, pixel_value)   ← only N² pixels per N×N block

            Decode:
              place sampled pixels at known positions
              fill gaps using scipy.interpolate.griddata  (nearest / linear / cubic)
            ```

            **Visual intuition:**
            ```
            Original 4×4 (N=2):        Sampled (every 2nd):     Interpolated:
            A B C D                     A . C .                  A A C C
            E F G H         →           . . . .         →        A A C C
            I J K L                     I . K .                  I I K K
            M N O P                     . . . .                  I I K K
            ```

            **Why it loses quality:** Interpolation guesses missing values — it works
            well for smooth regions but blurs sharp edges and fine texture.

            **Compression ratio:** N² (e.g. N=4 → 16×, N=8 → 64×)
            **Quality:** Depends on N and image smoothness
            **Type:** Lossy
            **Note:** Currently operates on grayscale (2D coordinate system)
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Downsampling (signal processing)](https://en.wikipedia.org/wiki/Downsampling_(signal_processing))")
            st.markdown("[Wikipedia — Image scaling / interpolation](https://en.wikipedia.org/wiki/Image_scaling)")
            st.markdown("[YouTube — Search: image subsampling interpolation](https://www.youtube.com/results?search_query=image+subsampling+interpolation+compression)")

    # ── DCT ────────────────────────────────────────────────────────────────────
    with st.expander("🌊 DCT — Discrete Cosine Transform / JPEG-style (5–20×)"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it does:** Converts image blocks from the *spatial domain* (pixel values)
            to the *frequency domain* (cosine wave amplitudes), then discards high-frequency
            components that the human eye barely notices.

            **This is the core idea behind JPEG.**

            **Step-by-step pipeline:**
            ```
            1. SPLIT  — divide image into 8×8 pixel blocks
            2. DCT    — apply 2D Discrete Cosine Transform to each block
                        [spatial pixels] → [64 frequency coefficients]
                        coefficient (0,0) = DC (average brightness)
                        coefficient (i,j) = amplitude of cosine wave at frequency (i,j)
            3. QUANTISE — divide each coefficient by a quality-dependent step size
                        Low frequencies (top-left) → fine steps  (preserve)
                        High frequencies (bottom-right) → coarse steps  (discard)
                        Many high-freq coefficients → 0  (run of zeros → compressible)
            4. ENCODE — store non-zero coefficients (float32 in this app; zigzag+
                        entropy coding in full JPEG)
            5. DECODE — reverse: dequantise → IDCT → reassemble blocks
            ```

            **DCT formula for a 1D block of N values:**
            ```
            X[k] = Σ x[n] · cos(π/N · (n + 0.5) · k)    k = 0…N-1
            ```

            **Why DCT beats Fourier for images:** DCT uses only real cosines (no complex
            numbers) and avoids the "ringing" artefacts of DFT at block boundaries.

            **Quality parameter (this app):**
            - `quality=1.0` → fine quantisation → low loss, moderate compression
            - `quality=0.1` → coarse quantisation → blocky artefacts, high compression

            **Compression ratio:** 5–20× depending on quality setting
            **Quality:** Adjustable (PSNR 20–45 dB)
            **Type:** Lossy
            **Note:** Currently operates on grayscale; real JPEG applies DCT per YCbCr channel
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform)")
            st.markdown("[Wikipedia — JPEG compression](https://en.wikipedia.org/wiki/JPEG)")
            st.markdown("[Wikipedia — Quantization (signal processing)](https://en.wikipedia.org/wiki/Quantization_(signal_processing))")
            st.markdown("[YouTube — Search: how JPEG compression works DCT](https://www.youtube.com/results?search_query=how+jpeg+compression+works+dct+explained)")
            st.markdown("[YouTube — Computerphile: JPEG](https://www.youtube.com/results?search_query=computerphile+how+jpeg+works)")

    # ── Comparison table ───────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📊 Algorithm Comparison")
    st.markdown("""
    | Algorithm | Type | Ratio | Quality | Best For | Worst On |
    |-----------|------|-------|---------|----------|----------|
    | Naive | Lossless | 1× | Perfect | Baseline only | — |
    | RLE | Lossless | 4–10× | Perfect | Solid regions, logos | Noise, photos |
    | Differential | Lossless | 2–5× | Perfect | Smooth gradients | High-freq noise |
    | Huffman | Lossless | 1.5–3× | Perfect | General purpose | Already-compressed data |
    | Sparse | Lossy | 10–50× | Variable | Quick preview | Sharp edges, text |
    | DCT | Lossy | 5–20× | Adjustable | Natural photos | Hard edges, text |
    """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Quality Metrics
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.header("📐 Quality & Compression Metrics")
    st.markdown("These metrics are computed on the **Diff** page after encode + decode.")

    # ── PSNR ───────────────────────────────────────────────────────────────────
    with st.expander("📡 PSNR — Peak Signal-to-Noise Ratio", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it measures:** How much noise (error) was introduced by compression,
            expressed as a ratio between the maximum possible signal and the error power.

            **Formula:**
            ```
            MSE  = mean( (original - reconstructed)² )
            PSNR = 10 · log₁₀(255² / MSE)              (dB)
            ```
            If MSE = 0 (perfect match), PSNR = ∞.

            **Interpretation guide:**
            | PSNR | Quality |
            |------|---------|
            | ∞ dB | Perfect — lossless reconstruction |
            | > 40 dB | Excellent — imperceptible difference |
            | 30–40 dB | Good — minor artefacts visible on close inspection |
            | 20–30 dB | Acceptable — noticeable artefacts |
            | < 20 dB | Poor — significant quality loss |

            **Limitation:** PSNR is a mathematical measure — it does not always match
            human perception. A blurry image and a sharp but shifted image might have the
            same PSNR but look very different to a person. SSIM addresses this.
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — PSNR](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio)")
            st.markdown("[YouTube — Search: PSNR image quality metric](https://www.youtube.com/results?search_query=PSNR+peak+signal+noise+ratio+image+quality)")

    # ── SSIM ───────────────────────────────────────────────────────────────────
    with st.expander("👁️ SSIM — Structural Similarity Index"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **What it measures:** Perceptual similarity — how similar two images *look*
            to a human viewer, accounting for luminance, contrast, and structure.

            **Formula (per local window):**
            ```
            SSIM(x,y) = [luminance] · [contrast] · [structure]
                      = (2μₓμᵧ + C₁)(2σₓᵧ + C₂)
                        ──────────────────────────────
                        (μₓ² + μᵧ² + C₁)(σₓ² + σᵧ² + C₂)
            ```
            where μ = local mean, σ = local variance, C₁/C₂ = stability constants.

            **Interpretation:**
            | SSIM | Meaning |
            |------|---------|
            | 1.0000 | Identical images |
            | > 0.95 | Very similar — differences barely visible |
            | > 0.90 | Similar — subtle differences |
            | 0.70–0.90 | Noticeable differences |
            | < 0.70 | Significant structural loss |

            **Advantage over PSNR:** SSIM is correlated with human visual perception.
            Blurring reduces SSIM more than a uniform brightness shift of the same MSE,
            matching how humans actually perceive image quality degradation.
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — SSIM](https://en.wikipedia.org/wiki/Structural_similarity_index_measure)")
            st.markdown("[YouTube — Search: SSIM structural similarity image quality](https://www.youtube.com/results?search_query=SSIM+structural+similarity+index+image+quality)")

    # ── Entropy & Efficiency ───────────────────────────────────────────────────
    with st.expander("⚡ Coding Efficiency — How Close to the Theoretical Limit?"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **Theoretical minimum bits:**
            ```
            Theoretical minimum = H(X) × N_pixels     (bits)
            ```

            **Coding efficiency:**
            ```
            Efficiency = Theoretical minimum / Actual compressed bits × 100%
            ```

            **Example:** An image with H(X) = 5.0 bits/pixel and 10,000 pixels has a
            theoretical minimum of 50,000 bits. If Huffman encodes it in 51,546 bits:
            ```
            Efficiency = 50,000 / 51,546 × 100% = 97.0%
            ```

            **Interpretation:**
            | Efficiency | Meaning |
            |------------|---------|
            | > 95% | Excellent — near-optimal |
            | 80–95% | Good |
            | 60–80% | Moderate — room for improvement |
            | < 60% | Low — significant overhead (headers, metadata) |

            **Why it's never 100%:** Real compressors have metadata overhead (code tables,
            shape info). Arithmetic coding can get very close; Huffman loses at most
            1 bit/symbol.
            """)
        with col2:
            st.markdown("**Learn more:**")
            st.markdown("[Wikipedia — Data compression ratio](https://en.wikipedia.org/wiki/Data_compression_ratio)")
            st.markdown("[Wikipedia — Kraft's inequality](https://en.wikipedia.org/wiki/Kraft%27s_inequality)")

    # ── BPP ────────────────────────────────────────────────────────────────────
    with st.expander("🔢 BPP — Bits Per Pixel"):
        st.markdown("""
        **What it measures:** How many bits of storage each pixel requires after compression.

        ```
        BPP = (compressed size in bytes × 8) / number of pixels
        ```

        **Reference values:**
        | BPP | Meaning |
        |-----|---------|
        | 8.0 | Uncompressed grayscale (1 byte per pixel) |
        | 24.0 | Uncompressed RGB (3 bytes per pixel) |
        | 0.5–2.0 | Good JPEG compression |
        | < 0.5 | Aggressive lossy compression |
        | ~H(X) | Ideal lossless (e.g. Huffman on a 5-bit-entropy image → 5 bpp) |

        **In the Diff page:** Shown as both *Original BPP* (always 8) and
        *Compressed BPP* (the achieved rate).

        [Wikipedia — Bits per pixel](https://en.wikipedia.org/wiki/Bit_depth)
        """)

    # ── MSE ────────────────────────────────────────────────────────────────────
    with st.expander("📏 MSE — Mean Squared Error"):
        st.markdown("""
        **What it measures:** The average squared difference between original and
        reconstructed pixel values. The foundation of PSNR.

        ```
        MSE = (1/N) · Σ (original_i - reconstructed_i)²
        ```

        **Properties:**
        - MSE = 0 → perfect reconstruction
        - MSE is sensitive to large errors (squaring penalises outliers heavily)
        - Lower is always better
        - Units: (pixel value)² — not directly interpretable; PSNR converts it to dB

        **Limitation:** Like PSNR, MSE doesn't match human perception well.
        Two images with the same MSE can look very different. Use together with SSIM
        for a complete picture.

        [Wikipedia — Mean squared error](https://en.wikipedia.org/wiki/Mean_squared_error)
        """)

    # ── Compression Ratio ─────────────────────────────────────────────────────
    with st.expander("📦 Compression Ratio & Space Saved"):
        st.markdown("""
        **Compression ratio:**
        ```
        Ratio = original size / compressed size
        ```
        A ratio of 4× means the compressed file is 4 times smaller than the original.

        **Space saved:**
        ```
        Space saved = (1 - 1/ratio) × 100%
        ```
        | Ratio | Space saved |
        |-------|-------------|
        | 1× | 0% |
        | 2× | 50% |
        | 4× | 75% |
        | 8× | 87.5% |
        | 16× | 93.75% |

        **Note:** Compression ratio can be < 1× (expansion) for noisy data compressed
        with RLE — the run-length pairs take more space than the raw bytes.

        [Wikipedia — Data compression ratio](https://en.wikipedia.org/wiki/Data_compression_ratio)
        """)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <em>"The fundamental problem of communication is that of reproducing at one point
    exactly or approximately a message selected at another." — Claude Shannon, 1948</em>
</div>
""", unsafe_allow_html=True)
