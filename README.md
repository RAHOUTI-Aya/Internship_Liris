# Internship LIRIS — OCR Pipeline for Historical Documents

OCR and LLM-based transcription pipeline for the *Dictionnaire de Trévoux* (1743), developed during an internship at **LIRIS, Lyon** 2026.

---

## Overview

This project compares OCR and vision-language models for transcribing 18th-century French dictionary pages, combined with a LLM post-correction step evaluated against manually validated gold standards.

---

## Models Tested

| Model | Type | CER | WER |
|---|---|---|---|
| Mistral OCR + Mistral Large | Cloud OCR + LLM | **0.0099** | **0.0426** |
| Qwen2.5-VL 7b (Ollama) | Local Vision LLM | 0.0740 | 0.1460 |
| GLM OCR | Web interface only | — | — |

---

## Pipeline

```text
Image (PNG)
    │
    ▼
[1] OCR Model             (Mistral OCR / Qwen2.5-VL)
    │
    ▼
[2] Markdown Cleaning
    │
    ▼
[3] LLM Post-Correction   
    │
    ▼
[4] Evaluation            (CER / WER vs gold standard)
```

---

## Repository Structure

```text
├── Documentation/          # Sphinx RST source files
├── Donnees/                # Input images and gold standard texts
├── Results/                # Evaluation output files
├── MistralOCR_Test.py      # Mistral OCR + Mistral Large pipeline
├── Qwen2_5vl_7b_Test.py    # Qwen2.5-VL local pipeline
└── utils.py                # Shared functions 
```

---

## Requirements

```bash
pip install requests mistralai
# For Qwen2.5-VL: install Ollama and run:
ollama pull qwen2.5vl:7b
```

---

## Documentation

Full documentation available on ReadTheDocs: [https://internship-liris.readthedocs.io/en/latest/]

---

## Author

Aya RAHOUTI — Internship at LIRIS, Lyon, 2026
