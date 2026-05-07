API Reference
=============

This page documents all functions in the pipeline script ``mistral2.py``.

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

   ocr_raw = run_mistral_ocr(r"C:\data\images\Pe.png")

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

   clean = clean_markdown(ocr_raw)

---

run_mistral_correction(ocr_text)
---------------------------------

.. code-block:: python

   def run_mistral_correction(ocr_text: str) -> str

Sends the cleaned OCR text to Mistral Large for post-correction.
The model fixes OCR errors while preserving archaic 18th-century French orthography.

Corrections applied:

- OCR character substitutions (``Vestigal`` → ``Vectigal``)
- Semantic word substitutions (``entre deux foires`` → ``entre deux soleils``)
- Erroneous modernisation (``portaient`` → ``portoient``)
- Corrupted proper nouns (``Bouleons`` → ``Boileau``)
- Wrong dates (``1587`` → ``1387``)
- Words split across line breaks

**Parameters**:

- ``ocr_text`` (*str*) — cleaned OCR text from ``clean_markdown()``

**Returns**:

- (*str*) — corrected plain text, single continuous line

**Raises**:

- ``ValueError`` — if the API response does not contain a ``choices`` field

**Example**:

.. code-block:: python

   corrected = run_mistral_correction(ocr_clean)

---

run_mistral_styling(corrected_text)
-------------------------------------

.. code-block:: python

   def run_mistral_styling(corrected_text: str) -> str

Sends the corrected text to Mistral Large for typographic enrichment.
The model adds XML-style tags reflecting the typographic conventions
of the *Dictionnaire de Trévoux*.

**Tags produced**:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Tag
     - Meaning
   * - ``<LC>...</LC>``
     - Large caps — article headwords (vedettes)
   * - ``<SC>...</SC>``
     - Small caps — author names, cross-references
   * - ``<IT>...</IT>``
     - Italic — titles, citations, abbreviations, foreign words
   * - ``<LA>...</LA>``
     - Latin text (nested inside ``<IT>`` when appropriate)
   * - ``<GR>...</GR>``
     - Greek text
   * - ``<HE>...</HE>``
     - Hebrew text
   * - ``<AU>...</AU>``
     - Author name cited as reference

**Parameters**:

- ``corrected_text`` (*str*) — corrected plain text from ``run_mistral_correction()``

**Returns**:

- (*str*) — enriched text with style tags, single continuous line

**Example**:

.. code-block:: python

   styled = run_mistral_styling(corrected)

---

normalize(text)
----------------

.. code-block:: python

   def normalize(text: str) -> str

Normalises a text string for evaluation. Strips style tags, lowercases,
resolves Unicode variants, and removes punctuation.

Applied to both gold standard and predictions before computing CER and WER.

**Parameters**:

- ``text`` (*str*) — raw or styled text string

**Returns**:

- (*str*) — normalised lowercase string, single line

**Example**:

.. code-block:: python

   gold_norm = normalize(gold_raw)
   pred_norm = normalize(corrected)

---

cer(gold, pred)
----------------

.. code-block:: python

   def cer(gold: str, pred: str) -> float

Computes the Character Error Rate between a gold string and a predicted string
using Levenshtein edit distance at character level.

.. math::

   \text{CER} = \frac{\text{editdistance}(gold, pred)}{|gold|}

**Parameters**:

- ``gold`` (*str*) — normalised gold standard string
- ``pred`` (*str*) — normalised prediction string

**Returns**:

- (*float*) — CER value between 0.0 (perfect) and 1.0+ (very poor)

**Example**:

.. code-block:: python

   score = cer(gold_norm, corr_norm)
   print(f"CER : {score:.4f}")

---

wer(gold, pred)
----------------

.. code-block:: python

   def wer(gold: str, pred: str) -> float

Computes the Word Error Rate between a gold string and a predicted string
using Levenshtein edit distance at word (token) level.

.. math::

   \text{WER} = \frac{\text{editdistance}(gold.split(), pred.split())}{|gold.split()|}

**Parameters**:

- ``gold`` (*str*) — normalised gold standard string
- ``pred`` (*str*) — normalised prediction string

**Returns**:

- (*float*) — WER value between 0.0 (perfect) and 1.0+ (very poor)

**Example**:

.. code-block:: python

   score = wer(gold_norm, corr_norm)
   print(f"WER : {score:.4f}")