API Reference
=============

This page documents all functions in the pipeline script ``MistralOCR.py``.

run_mistral_ocr(image_path)
----------------------------

.. code-block:: python

   def run_mistral_ocr(image_path: str) -> str

Sends a PNG image to the Mistral OCR API and returns the raw Markdown transcription.

**Parameters**:

- ``image_path`` (*str*) — absolute or relative path to the PNG image file

**Returns**:

- (*str*) — raw Markdown text concatenated from all pages returned by the API

**Raises**:

- ``ValueError`` — if the API response does not contain a ``pages`` field

**Example**:

.. code-block:: python

   ocr_raw = run_mistral_ocr("page_1905.png")

---

clean_markdown(text)
---------------------

.. code-block:: python

   def clean_markdown(text: str) -> str

Removes all Markdown markup from a string and returns plain continuous text on a single line.

Specifically removes: embedded images (``![](...)``), heading markers (``#``),
bold and italic markers (``*``, ``_``), HTML entities (``&amp;``, ``&lt;``, ``&gt;``),
inline links, and inline code. All newlines are replaced with spaces.

**Parameters**:

- ``text`` (*str*) — raw Markdown string from the OCR stage

**Returns**:

- (*str*) — cleaned plain text, single line, no extra whitespace

**Example**:

.. code-block:: python

   ocr_clean = clean_markdown(ocr_raw)

---

run_mistral_correction(ocr_text)
---------------------------------

.. code-block:: python

   def run_mistral_correction(ocr_text: str) -> str

Sends the cleaned OCR text to Mistral Large (``mistral-large-latest``, temperature 0)
for post-correction. The model fixes OCR errors while preserving archaic
18th-century French orthography.

Corrections applied:

- OCR character substitutions (``Vestigal`` → ``Vectigal``)
- Semantic word substitutions (``entre deux foires`` → ``entre deux soleils``)
- Erroneous modernisation of archaic spelling (``portaient`` → ``portoient``)
- Corrupted proper nouns (``Bouleons`` → ``Boileau``, ``Genili`` → ``Generoso``)
- Wrong dates (``1587`` → ``1387``, ``1688`` → ``1388``)
- Words split across line breaks

**Parameters**:

- ``ocr_text`` (*str*) — cleaned OCR text from ``clean_markdown()``

**Returns**:

- (*str*) — corrected plain text, single continuous line, no newlines

**Raises**:

- ``ValueError`` — if the API response does not contain a ``choices`` field

**Example**:

.. code-block:: python

   corrected = run_mistral_correction(ocr_clean)

---

normalize(text)
----------------

.. code-block:: python

   def normalize(text: str) -> str

Normalises a text string before computing evaluation metrics.
Applied identically to both the gold standard and the predictions
to ensure fair comparison.

Operations performed:

- Unicode NFKD normalisation
- Lowercase conversion
- Long ``ſ`` → ``s``, ``œ`` → ``oe``, ``æ`` → ``ae``
- Removal of punctuation (``.,;:!?()[]"'&``)
- Collapsing of multiple spaces into one

**Parameters**:

- ``text`` (*str*) — raw or corrected text string

**Returns**:

- (*str*) — normalised lowercase string, single line

**Example**:

.. code-block:: python

   gold_norm = normalize(gold_raw)
   ocr_norm  = normalize(ocr_clean)
   corr_norm = normalize(corrected)

---

cer(gold, pred)
----------------

.. code-block:: python

   def cer(gold: str, pred: str) -> float

Computes the Character Error Rate between a gold string and a predicted string
using Levenshtein edit distance at character level.

.. math::

   \text{CER} = \frac{\text{editdistance}_{char}(gold, pred)}{|gold|}

**Parameters**:

- ``gold`` (*str*) — normalised gold standard string
- ``pred`` (*str*) — normalised prediction string

**Returns**:

- (*float*) — CER value between 0.0 (perfect) and 1.0+ (very poor)

**Example**:

.. code-block:: python

   cer_ocr  = cer(gold_norm, ocr_norm)
   cer_corr = cer(gold_norm, corr_norm)
   print(f"CER : {cer_corr:.4f}")

---

wer(gold, pred)
----------------

.. code-block:: python

   def wer(gold: str, pred: str) -> float

Computes the Word Error Rate between a gold string and a predicted string
using Levenshtein edit distance at word (token) level.

.. math::

   \text{WER} = \frac{\text{editdistance}_{word}(gold.split(), pred.split())}{|gold.split()|}

**Parameters**:

- ``gold`` (*str*) — normalised gold standard string
- ``pred`` (*str*) — normalised prediction string

**Returns**:

- (*float*) — WER value between 0.0 (perfect) and 1.0+ (very poor)

**Example**:

.. code-block:: python

   wer_ocr  = wer(gold_norm, ocr_norm)
   wer_corr = wer(gold_norm, corr_norm)
   print(f"WER : {wer_corr:.4f}")

---

levenshtein_chars(a, b)
------------------------

.. code-block:: python

   def levenshtein_chars(a: str, b: str) -> int

Computes the Levenshtein edit distance between two strings at **character** level.
Used internally by ``cer()``.

**Parameters**:

- ``a`` (*str*) — first string
- ``b`` (*str*) — second string

**Returns**:

- (*int*) — minimum number of single-character edits (insertions, deletions, substitutions)

---

levenshtein_words(a, b)
------------------------

.. code-block:: python

   def levenshtein_words(a: list, b: list) -> int

Computes the Levenshtein edit distance between two **token lists**.
Used internally by ``wer()``.

**Parameters**:

- ``a`` (*list*) — first token list (from ``str.split()``)
- ``b`` (*list*) — second token list

**Returns**:

- (*int*) — minimum number of word-level edits (insertions, deletions, substitutions)