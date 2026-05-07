Models
======

This project compares three OCR/vision models for the transcription stage,
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

**Limitations**:

- May truncate long pages if output exceeds token limits
- Returns Markdown markup (italics, bold, headers) that must be cleaned
- Cloud API: requires internet access and a valid Mistral API key

**Input format**:

.. code-block:: python

   {
     "model": "mistral-ocr-latest",
     "document": {
       "type": "image_url",
       "image_url": "data:image/png;base64,<base64>"
     }
   }

**Output format**: JSON with a ``pages`` list, each page containing a ``markdown`` field.

---

Pixtral-12b
-----------

**Type**: Vision-language model / multimodal LLM (cloud)

**Endpoint**: ``https://api.mistral.ai/v1/chat/completions``

**Model ID**: ``pixtral-12b-2409``

Pixtral-12b is Mistral AI's 12-billion parameter multimodal model capable of processing
images alongside text prompts. It is used here as a vision LLM: the image is sent in
the chat payload and the model is prompted to transcribe its content.

**Strengths**:

- Flexible: transcription behaviour is fully controlled via the prompt
- Can apply corrections and normalisation in a single pass
- No separate cleaning step required if the prompt instructs plain text output

**Limitations**:

- Higher risk of hallucination than a dedicated OCR model
- Prone to truncating output on long pages (no explicit ``max_tokens`` by default)
- Slower and more expensive per page than Mistral OCR
- Output quality is heavily prompt-dependent

**Input format**:

.. code-block:: python

   {
     "model": "pixtral-12b-2409",
     "messages": [
       {
         "role": "user",
         "content": [
           {"type": "text", "text": "<prompt>"},
           {"type": "image_url", "image_url": "data:image/png;base64,<base64>"}
         ]
       }
     ],
     "max_tokens": 4096,
     "temperature": 0
   }

**Output format**: standard chat completion JSON, ``choices[0].message.content``.

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
- Competitive performance with larger cloud models on structured document tasks
- Free and open-source (Apache 2.0 licence)

**Limitations**:

- Requires a machine with sufficient VRAM (minimum 8 GB recommended)
- Slower inference than cloud APIs on CPU-only setups
- Output quality depends on hardware; GPU strongly recommended
- Must be pulled before first use: ``ollama pull qwen2.5vl:7b``

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

Regardless of the OCR model used in stage 1, all transcriptions pass through
**Mistral Large** for post-correction. This step fixes:

- OCR substitution errors (``Vestigal`` → ``Vectigal``)
- Semantic errors (``entre deux foires`` → ``entre deux soleils``)
- Erroneous modernisation of archaic spelling
- Corrupted proper nouns and dates
- Words split across line breaks

The same Mistral Large model is also used for the optional typographic enrichment stage (stage 4).

Model Comparison Summary
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 15 15 20

   * - Model
     - Type
     - Local / Cloud
     - API Key needed
     - Cost
     - Prompt needed
   * - Mistral OCR
     - Dedicated OCR
     - Cloud
     - Yes (Mistral)
     - Paid
     - No
   * - Pixtral-12b
     - Vision LLM
     - Cloud
     - Yes (Mistral)
     - Paid
     - Yes
   * - Qwen2.5-VL 7b
     - Vision LLM
     - Local
     - No
     - Free
     - Yes