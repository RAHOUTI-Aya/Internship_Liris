OCR Pipeline Description
========================

The pipeline is composed of four main steps:

1. OCR Extraction
-----------------
We use Mistral OCR to extract text from scanned images:

- Input: image (PNG/JPG)
- Output: markdown-like raw text

2. Markdown Cleaning
--------------------
The extracted text is cleaned using regex:
- removal of markdown syntax
- removal of line breaks
- normalization of spacing

3. LLM Post-Correction
----------------------
Mistral Large is used to correct OCR errors while preserving
historical spelling conventions.

Key rules:
- preserve archaic French spelling
- correct OCR noise
- fix word segmentation errors

4. Evaluation
-------------
We compare OCR output and corrected text against a gold standard
using CER and WER metrics.