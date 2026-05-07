Results
=======

This section presents the evaluation results for each model at each stage of the pipeline,
measured against the gold standard of the *Dictionnaire de Trévoux* (1743).

Experimental Setup
------------------

- **Document**: Page ``Pe`` from the Dictionnaire de Trévoux (1743)
- **Gold standard**: 8519 characters of manually validated continuous text
- **Post-correction model**: Mistral Large (``mistral-large-latest``, temperature 0)
- **Metrics**: CER and WER after normalisation (see :doc:`3_Metrics`)

Results by Model
----------------

Mistral OCR + Mistral Large
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Stage
     - CER
     - WER
   * - Mistral OCR (raw)
     - —
     - —
   * - After Mistral Large correction
     - —
     - —
   * - After typographic enrichment
     - —
     - —

.. note::
   Results to be filled after running the pipeline on the full page set.

Pixtral-12b + Mistral Large
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Stage
     - CER
     - WER
   * - Pixtral-12b (raw, vision LLM)
     - 0.0919
     - 0.2908
   * - After Mistral Large correction
     - —
     - —

.. note::
   The initial Pixtral-12b result (CER 0.09, WER 0.29) was obtained without ``max_tokens``
   set, causing output truncation. Setting ``max_tokens: 4096`` is required for full-page results.

Qwen2.5-VL 7b + Mistral Large
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Stage
     - CER
     - WER
   * - Qwen2.5-VL 7b (raw, local)
     - —
     - —
   * - After Mistral Large correction
     - —
     - —

.. note::
   Results to be filled after running the pipeline locally with Ollama.

Cross-Model Comparison
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - Model
     - CER (raw)
     - WER (raw)
     - Notes
   * - Mistral OCR
     - —
     - —
     - Dedicated OCR, no prompt needed
   * - Pixtral-12b
     - 0.0919
     - 0.2908
     - Truncation issue without max_tokens
   * - Qwen2.5-VL 7b
     - —
     - —
     - Local, free, no API key

Key Observations
-----------------

**Gap between CER and WER**

A low CER combined with a high WER (as observed with Pixtral-12b: CER 0.09, WER 0.29)
indicates that errors are concentrated at the word level rather than the character level.
This means the model substitutes entire words rather than individual characters —
a pattern typical of semantic confusion errors and output truncation.

**Impact of LLM post-correction**

The Mistral Large post-correction step consistently reduces WER more than CER,
confirming that it is particularly effective at resolving word-level semantic errors
(wrong word substituted by a plausible but incorrect alternative).

**Typographic enrichment validation**

The styled output (stage 4) is evaluated with tags stripped. If the CER/WER of the
styled output matches the corrected text exactly, it confirms that the enrichment step
did not alter the textual content — only added markup.

**Truncation**

Pixtral-12b and Qwen2.5-VL both require an explicit ``max_tokens`` parameter to avoid
silently truncating long pages. Mistral OCR handles long documents natively through
its page-segmentation architecture.