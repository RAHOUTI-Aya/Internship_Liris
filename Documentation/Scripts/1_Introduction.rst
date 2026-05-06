Introduction
============

This project aims to evaluate the performance of an OCR system applied to
historical French documents from the 18th century.

The main challenges include:

- Old orthography (e.g. "portoient", "appelloit")
- Non-standard punctuation and spelling
- Degraded scan quality
- Historical vocabulary

We propose a pipeline combining:

1. Mistral OCR for raw text extraction
2. Cleaning and normalization
3. LLM-based correction using Mistral Large
4. Evaluation using CER and WER metrics