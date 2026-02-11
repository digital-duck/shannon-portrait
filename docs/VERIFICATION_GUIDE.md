# Shannon Portrait - Verification & Testing Guide

## 📋 Complete Verification Checklist

This guide provides step-by-step instructions to verify all functionality before committing to GitHub.

---

## 🚀 Quick Start Verification (5 minutes)

### Step 1: Extract and Install

```bash
# Extract the project
tar -xzf shannon-portrait-complete.tar.gz
cd shannon-portrait

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

**Expected Output:**
```
Successfully installed shannon-portrait-0.1.0
```

### Step 2: Verify Installation

```bash
# Check command is available
infocodec --version

# Get help
infocodec --help
```

**Expected Output:**
```
Version: 0.1.0

Usage: infocodec [OPTIONS] COMMAND [ARGS]...

Commands:
  encode     Encode (compress) input data
  decode     Decode (decompress) compressed data
  benchmark  Benchmark multiple compression methods
  ui         Launch Streamlit UI
```

---

## 🧪 Unit Tests (10 minutes)

### Run All Tests

```bash
# Install pytest if not already installed
pip install pytest pytest-cov

# Run all tests with coverage
pytest tests/ -v --cov=infocodec --cov-report=term

# Or run specific test files
pytest tests/test_compressors.py -v
pytest tests/test_reconstructors.py -v
pytest tests/test_metrics.py -v
```

### Expected Test Results

```
tests/test_compressors.py::TestCompressors
✓ test_all_compressors_exist                    PASSED
✓ test_naive_compressor                         PASSED
✓ test_rle_compressor                          PASSED
✓ test_differential_compressor                 PASSED
✓ test_huffman_compressor                      PASSED
✓ test_sparse_compressor                       PASSED
✓ test_dct_compressor                          PASSED
✓ test_compression_ratio_ordering              PASSED
✓ test_metadata_completeness                   PASSED
[... more tests ...]

tests/test_reconstructors.py::TestReconstructors
✓ test_all_reconstructors_exist                PASSED
✓ test_round_trip_lossless                     PASSED
✓ test_round_trip_lossy                        PASSED
[... more tests ...]

tests/test_metrics.py::TestEntropyCalculation
✓ test_entropy_uniform                         PASSED
✓ test_entropy_binary                          PASSED
✓ test_entropy_random                          PASSED
[... more tests ...]

======================== XX passed in X.XXs ========================
Coverage: 85%+
```

### Test Breakdown

| Test Suite | Tests | What It Verifies |
|------------|-------|------------------|
| `test_compressors.py` | 15+ | All 6 compression methods work correctly |
| `test_reconstructors.py` | 12+ | All 6 reconstruction methods work correctly |
| `test_metrics.py` | 15+ | Entropy, PSNR, SSIM calculations are correct |

---

## 🖥️ CLI Verification (15 minutes)

### Test 1: Encode Command

```bash
# Create a test image
python -c "from infocodec.utils.image_utils import create_test_image, save_image; save_image(create_test_image(pattern='blocks'), 'test_blocks.png')"

# Test each compression method
infocodec encode --input test_blocks.png --method naive --output test_naive.dat -v
infocodec encode --input test_blocks.png --method rle --output test_rle.dat -v
infocodec encode --input test_blocks.png --method differential --output test_diff.dat -v
infocodec encode --input test_blocks.png --method huffman --output test_huff.dat -v
infocodec encode --input test_blocks.png --method sparse --output test_sparse.dat -v
infocodec encode --input test_blocks.png --method dct --output test_dct.dat -v

# Test auto-detection
infocodec encode --input test_blocks.png --method auto --output test_auto.dat -v
```

**Expected Output (for each):**
```
🔄 Encoding: test_blocks.png
📎 Media type: image
⚡ Compressing with [method]...

✅ Compression complete!
   Time: 0.XXXs
   Original: 4,096 bytes
   Compressed: XXX bytes
   Ratio: X.XXx
   Output: test_[method].dat
```

**Verification Checklist:**
- [ ] All 6 methods complete without errors
- [ ] Compressed files are created (.dat and .json)
- [ ] Compression ratios make sense:
  - RLE on blocks: > 3x
  - Huffman: 1.2-1.5x
  - Sparse: > 10x
  - DCT: 3-8x

### Test 2: Decode Command

```bash
# Decode each compressed file
infocodec decode --input test_naive.dat --output recon_naive.png -v
infocodec decode --input test_rle.dat --output recon_rle.png -v
infocodec decode --input test_diff.dat --output recon_diff.png -v
infocodec decode --input test_huff.dat --output recon_huff.png -v
infocodec decode --input test_sparse.dat --output recon_sparse.png -v
infocodec decode --input test_dct.dat --output recon_dct.png -v
```

**Expected Output (for each):**
```
🔄 Decoding: test_[method].dat
⚡ Decompressing with [Method]...

✅ Decompression complete!
   Time: 0.XXXs
   Method: [Method]
   Output: recon_[method].png
   Shape: (64, 64)
```

**Verification Checklist:**
- [ ] All files decode successfully
- [ ] Reconstructed images are created
- [ ] Lossless methods (naive, rle, differential, huffman) produce identical images
- [ ] Lossy methods (sparse, dct) produce reasonable quality images

### Test 3: Benchmark Command

```bash
# Benchmark all methods
infocodec benchmark --input test_blocks.png --methods all --format table

# Save results
infocodec benchmark --input test_blocks.png --methods all --output results/ --format json
```

**Expected Output:**
```
🔬 Benchmarking: test_blocks.png

Testing naive... ✓ 1.00x in 0.XXXs
Testing rle... ✓ 4.XXx in 0.XXXs
Testing differential... ✓ 2.XXx in 0.XXXs
Testing huffman... ✓ 1.XXx in 0.XXXs
Testing sparse... ✓ 16.XXx in 0.XXXs
Testing dct... ✓ 5.XXx in 0.XXXs

================================================================================
BENCHMARK RESULTS
================================================================================

Method           | Original   | Compressed | Ratio    | Time     | Entropy
-------------------------------------------------------------------------------
naive            |      4,096 |      4,096 |   1.00x  |  0.XXXs  |  5.XX
rle              |      4,096 |      1,024 |   4.00x  |  0.XXXs  |  5.XX
differential     |      4,096 |      X,XXX |   X.XXx  |  0.XXXs  |  5.XX
huffman          |      4,096 |      X,XXX |   X.XXx  |  0.XXXs  |  5.XX
sparse           |      4,096 |        XXX |  16.XXx  |  0.XXXs  |  5.XX
dct              |      4,096 |      X,XXX |   X.XXx  |  0.XXXs  |  5.XX
```

**Verification Checklist:**
- [ ] All methods complete
- [ ] Ratios are reasonable for the pattern
- [ ] Results saved to JSON file

### Test 4: Image Pattern Tests

Test with different patterns to verify method selection:

```bash
# Create different patterns
python -c "from infocodec.utils.image_utils import create_test_image, save_image; save_image(create_test_image(pattern='gradient'), 'gradient.png')"
python -c "from infocodec.utils.image_utils import create_test_image, save_image; save_image(create_test_image(pattern='noise'), 'noise.png')"

# Benchmark each
infocodec benchmark --input gradient.png --methods all
infocodec benchmark --input noise.png --methods all
```

**Expected Behavior:**
- **Gradient**: Differential should perform best (5-10x)
- **Blocks**: RLE should perform best (4-10x)
- **Noise**: All methods should compress poorly (~1x or less)

---

## 🎨 Streamlit UI Verification (20 minutes)

### Launch UI

```bash
# Start Streamlit
streamlit run infocodec/ui/InfoCoDec.py

# Or use CLI shortcut
infocodec-ui
```

Browser should open at: http://localhost:8501

### Page 1: Settings (⚙️)

**Checklist:**
- [ ] Page loads without errors
- [ ] Algorithm dropdown works (auto, naive, rle, etc.)
- [ ] Quality slider works (0.0 - 1.0)
- [ ] Block size selector works (4, 8, 16, 32)
- [ ] Cache enable/disable toggle works
- [ ] OpenRouter API key field present
- [ ] Model selection dropdown works
- [ ] Temperature slider works (0.0 - 1.0)
- [ ] Max tokens input works
- [ ] Settings saved to session state

**Test:**
1. Change compression method to "huffman"
2. Set quality to 0.8
3. Enter a test API key
4. Select "anthropic/claude-3.5-sonnet"
5. Click "Save All Settings"
6. Check that settings persist when navigating to other pages

### Page 2: Encode (📤)

**Checklist:**
- [ ] Page loads without errors
- [ ] "Upload Image" option works
- [ ] "Generate Test Pattern" option works
- [ ] Pattern selector works (gradient, blocks, noise, checkerboard)
- [ ] Size slider works (32-256)
- [ ] Generated image displays correctly
- [ ] Image info expander shows:
  - [ ] Entropy value
  - [ ] Size (height × width)
  - [ ] Total pixels
  - [ ] Unique values
  - [ ] Min/Max values
  - [ ] Pixel distribution chart
- [ ] Compression method selector works
- [ ] "Compress" button works
- [ ] Compression results display:
  - [ ] Original size
  - [ ] Compressed size
  - [ ] Compression ratio
  - [ ] Entropy
- [ ] Download button works (downloads .dat file)

**Test Workflow:**
1. Select "Generate Test Pattern"
2. Choose "blocks" pattern
3. Set size to 128
4. Click "Generate Pattern"
5. Verify image displays
6. Select compression method "rle"
7. Click "Compress"
8. Verify compression ratio > 3x
9. Click download button
10. Verify .dat file downloads

### Page 3: Decode (📥)

**Checklist:**
- [ ] Page loads without errors
- [ ] Detects encoded data from Encode page
- [ ] Shows compressed data info:
  - [ ] Method
  - [ ] Compressed size
  - [ ] Original shape
- [ ] Shows original image for reference
- [ ] "Reconstruct" button works
- [ ] Reconstructed image displays correctly
- [ ] Quality metrics display:
  - [ ] PSNR (with interpretation)
  - [ ] SSIM
  - [ ] MSE
- [ ] Side-by-side comparison works:
  - [ ] Original
  - [ ] Reconstructed
  - [ ] Difference (amplified)
- [ ] Quality interpretation correct:
  - [ ] Perfect for lossless
  - [ ] Excellent/Good/Acceptable for lossy

**Test Workflow:**
1. After encoding (from Encode page)
2. Navigate to Decode page
3. Verify data is automatically loaded
4. Click "Reconstruct"
5. Verify reconstructed image appears
6. Check PSNR value:
   - For lossless (naive, rle, differential, huffman): ∞
   - For lossy (sparse, dct): finite but > 20 dB
7. Compare side-by-side images

### Page 4: Diff (📊)

**Checklist:**
- [ ] Page loads without errors
- [ ] Requires encode + decode data (shows warning if missing)
- [ ] Top metrics display correctly:
  - [ ] Compression ratio
  - [ ] PSNR
  - [ ] SSIM
  - [ ] Space saved
  - [ ] Efficiency
- [ ] Tab 1: Visual Analysis
  - [ ] Side-by-side comparison (original, reconstructed, difference)
  - [ ] Error heatmap displays
  - [ ] Error histogram displays
- [ ] Tab 2: Statistical Analysis
  - [ ] Original distribution stats
  - [ ] Reconstructed distribution stats
  - [ ] Pixel value histograms (overlaid)
  - [ ] Pixel correlation scatter plot
- [ ] Tab 3: Information Theory
  - [ ] Entropy analysis (original, reconstructed, reduction)
  - [ ] Compression analysis (BPP, ratio)
  - [ ] Theoretical limits (minimum bits, efficiency)
  - [ ] Efficiency interpretation correct
- [ ] Tab 4: Report
  - [ ] Formatted text report displays
  - [ ] Download TXT button works
  - [ ] Download JSON button works

**Test Workflow:**
1. Complete Encode and Decode steps first
2. Navigate to Diff page
3. Verify all 5 top metrics display
4. Go through each tab:
   - Visual: Check all charts render
   - Statistical: Verify distributions make sense
   - Information Theory: Check efficiency calculation
   - Report: Download both TXT and JSON
5. Verify downloads contain correct data

### Common UI Issues to Check

**If page doesn't load:**
```bash
# Check for errors in terminal
# Look for missing imports or syntax errors
```

**If images don't display:**
- Check that numpy arrays are uint8
- Verify shape is (H, W) not (H, W, 1)
- Check clamp parameter is True

**If metrics show NaN or Inf unexpectedly:**
- Check for division by zero
- Verify image data is valid
- Check that compression actually ran

---

## 📊 Data Validation (10 minutes)

### Verify Compression Characteristics

Create a validation script:

```python
# validation_test.py
from infocodec.core.compressors import COMPRESSORS
from infocodec.core.reconstructors import RECONSTRUCTORS
from infocodec.core.metrics import calculate_psnr
from infocodec.utils.image_utils import create_test_image

def validate_method(method_name, pattern, expected_ratio_min):
    """Validate a compression method"""
    print(f"\n Testing {method_name} on {pattern}...")
    
    # Create image
    image = create_test_image(size=(64, 64), pattern=pattern)
    
    # Compress
    compressor = COMPRESSORS[method_name]()
    compressed, metadata = compressor.compress(image)
    stats = compressor.get_stats()
    
    # Reconstruct
    reconstructor = RECONSTRUCTORS[method_name]()
    reconstructed = reconstructor.reconstruct(compressed, metadata)
    
    # Check
    psnr = calculate_psnr(image, reconstructed)
    ratio = stats['compression_ratio']
    
    print(f"   Compression: {ratio:.2f}x")
    print(f"   PSNR: {psnr:.2f} dB")
    
    # Validate
    assert ratio >= expected_ratio_min, f"Ratio too low: {ratio}"
    if method_name in ['naive', 'rle', 'differential', 'huffman']:
        assert psnr == float('inf'), f"Lossless should be perfect"
    else:
        assert psnr > 20, f"Lossy quality too low: {psnr}"
    
    print("   ✓ PASSED")

# Run validations
validate_method('rle', 'blocks', 3.0)  # RLE on blocks: >3x
validate_method('differential', 'gradient', 2.0)  # Diff on gradient: >2x
validate_method('huffman', 'blocks', 1.2)  # Huffman: >1.2x
validate_method('sparse', 'gradient', 10.0)  # Sparse: >10x

print("\n✓ All validations passed!")
```

Run it:
```bash
python validation_test.py
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'infocodec'
```

**Solution:**
```bash
# Make sure you're in the project root
cd shannon-portrait

# Reinstall in editable mode
pip install -e .
```

### Issue 2: Missing Dependencies

**Symptom:**
```
ModuleNotFoundError: No module named 'scipy'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 3: Streamlit Won't Start

**Symptom:**
```
streamlit: command not found
```

**Solution:**
```bash
pip install streamlit
```

### Issue 4: Tests Fail

**Symptom:**
```
FAILED tests/test_compressors.py::test_rle_compressor
```

**Solution:**
- Check test output for specific assertion failure
- Verify the algorithm implementation
- Check that test data is being generated correctly

### Issue 5: Decode Fails

**Symptom:**
```
KeyError: 'huffman_codes'
```

**Solution:**
- Ensure metadata is being saved correctly in encode
- Check that metadata is being read correctly in decode
- Verify JSON serialization of metadata

---

## ✅ Final Checklist Before Commit

### Code Quality
- [ ] All unit tests pass
- [ ] No syntax errors in any file
- [ ] All imports work correctly
- [ ] No print statements left in (use logging instead)
- [ ] Docstrings present for all public functions

### Functionality
- [ ] All 6 compression methods work
- [ ] All 6 reconstruction methods work
- [ ] CLI encode/decode/benchmark work
- [ ] Streamlit UI loads all pages
- [ ] Settings persist across pages
- [ ] Encode → Decode → Diff workflow works

### Documentation
- [ ] README.md is complete
- [ ] INSTALL.md has clear instructions
- [ ] Code comments are present
- [ ] Examples work as documented

### Files to Include
- [ ] All source code (.py files)
- [ ] Tests (tests/ directory)
- [ ] Documentation (.md files)
- [ ] Requirements (requirements.txt, setup.py, pyproject.toml)
- [ ] Configuration (.env.example, .gitignore)

### Files to Exclude
- [ ] `__pycache__/` directories
- [ ] `.pyc` files
- [ ] Virtual environments (`venv/`, `env/`)
- [ ] Test outputs (`.dat`, `.png` test files)
- [ ] Personal API keys (`.env` file)

---

## 🚀 Ready to Commit!

Once all checks pass:

```bash
# Initialize git (if not already)
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Shannon Portrait - InfoCodec v0.1.0

- 6 compression algorithms (naive, rle, differential, huffman, sparse, dct)
- 6 reconstruction algorithms
- Complete CLI (encode, decode, benchmark, ui)
- Streamlit multi-page UI (Settings, Encode, Decode, Diff)
- Comprehensive metrics (Shannon entropy, PSNR, SSIM)
- Full test suite with 40+ tests
- Documentation and examples"

# Push to GitHub
git remote add origin https://github.com/yourusername/shannon-portrait.git
git branch -M main
git push -u origin main
```

---

## 📈 Test Coverage Goal

Aim for:
- **Overall Coverage**: > 85%
- **Core Algorithms**: > 90%
- **Metrics**: > 95%
- **UI**: > 60% (harder to test)

Run coverage report:
```bash
pytest --cov=infocodec --cov-report=html
open htmlcov/index.html  # View detailed report
```

---

**Congratulations! Your Shannon Portrait project is production-ready!** 🎉
