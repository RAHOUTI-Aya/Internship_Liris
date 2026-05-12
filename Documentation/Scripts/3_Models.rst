Models
======

This project compares two OCR/vision models for the transcription stage,
all followed by the same Mistral Large post-correction step.

Mistral OCR
-----------

**Type**: Dedicated OCR API (cloud)

**Endpoint**: ``https://api.mistral.ai/v1/ocr``

**Model ID**: ``mistral-ocr-latest``

Mistral OCR is a specialised optical character recognition model developed by Mistral AI.
Unlike general vision-language models, it is optimised for document transcription and
returns structured Markdown output with page-level segmentation.

**Strengths**:

- High accuracy on printed text including historical fonts
- Returns structured ``pages`` objects with per-page Markdown
- Handles multi-column layouts better than general vision models
- No prompt required: document is sent directly
- Best CER/WER scores observed across all tested models

**Limitations**:

- Returns Markdown markup (italics, bold, headers) that must be cleaned before evaluation
- Cloud API: requires internet access and a valid Mistral API key
- Paid service

**Input format**:

.. code-block:: python

   {
     "model": "mistral-ocr-latest",
     "document": {
       "type": "image_url",
       "image_url": "data:image/png;base64,<base64>"
     }
   }

**Output format**: JSON with a ``pages`` list, each page containing a ``markdown`` field. Or Raw text.

---

Qwen2.5-VL 7b (Ollama)
-----------------------

**Type**: Vision-language model (local, open-source)

**Endpoint**: ``http://localhost:11434/api/chat``

**Model ID**: ``qwen2.5vl:7b``

Qwen2.5-VL is an open-source vision-language model developed by Alibaba DAMO Academy.
The 7b variant is run locally via **Ollama**, requiring no API key or internet connection
after the initial model download.

**Strengths**:

- Fully local: no data leaves the machine, no API cost
- Strong multilingual capability including French and Latin
- Free and open-source (Apache 2.0 licence)
- Correctly transcribes most running text

**Limitations**:

- Requires a machine with sufficient VRAM (minimum 8 GB recommended)
- Slower inference than cloud APIs on CPU-only setups
- Post-correction step had no effect on this model (ΔCER: 0.000, ΔWER: 0.000),
  suggesting the LLM correction prompt needs to be adapted for Qwen outputs
- Produces hallucinated artefacts on degraded page regions
  (e.g. ``"us de F Provence, paye quoral, po Les Enfantras"``)
- Includes page headers and column markers in output (e.g. ``"Tome V. P E A."``)

**Setup**:

.. code-block:: bash

   # Install Ollama (https://ollama.com)
   ollama pull qwen2.5vl:7b
   ollama serve   # starts the local API on port 11434

**Input format**:

.. code-block:: python

   {
     "model": "qwen2.5vl:7b",
     "messages": [
       {
         "role": "user",
         "content": [
           {"type": "text", "text": "<prompt>"},
           {"type": "image_url", "image_url": "data:image/png;base64,<base64>"}
         ]
       }
     ],
     "stream": False
   }

**Output format**: ``message.content`` string in the Ollama chat response.

---

Post-Correction: Mistral Large
-------------------------------

**Type**: LLM text correction (cloud)

**Endpoint**: ``https://api.mistral.ai/v1/chat/completions``

**Model ID**: ``mistral-large-latest``

Transcriptions pass through
**Mistral Large** for post-correction. This step fixes:

- OCR character substitutions (``Vestigal`` → ``Vectigal``)
- Semantic errors (``entre deux foires`` → ``entre deux soleils``)
- Erroneous modernisation of archaic spelling (``portaient`` → ``portoient``)
- Corrupted proper nouns and dates
- Words split across line breaks

.. note::
   The post-correction step proved highly effective on Mistral OCR output (ΔWER up to +0.0422).


Model Comparison Summary
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 15 20

   * - Model
     - Type
     - Local / Cloud
     - API Key needed
     - Cost
   * - Mistral OCR
     - Dedicated OCR
     - Cloud
     - Yes (Mistral)
     - Paid
   * - Qwen2.5-VL 7B
     - Vision LLM
     - Local
     - No
     - Free

Kraken+Ciaconna
-----------

Kraken+Ciaconna has shown remarkable performance on Latin and polytonic Greek scripts.

.. figure:: /Documentation/Images/table_ref.png
   :width: 100%
   :align: center
   :alt: Alternative text for the image
   :name: table_ref

Results of Matteo Romanello, Sven Najem-Meyer, and Bruce Robertson. 2021. Optical Character Recognition of 19th Century Classical Commentaries: the Current State of Affairs.

