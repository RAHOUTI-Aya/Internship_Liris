Evaluation Metrics
==================

Character Error Rate (CER)
--------------------------

CER measures the number of character-level edits required:

- insertions
- deletions
- substitutions

Formula:
CER = Levenshtein_distance / number_of_characters

Word Error Rate (WER)
---------------------

WER measures errors at word level:

WER = Levenshtein_distance_words / number_of_words_in_reference

These metrics are used to evaluate OCR accuracy before and after correction.

Normalisation Before Evaluation
---------------------------------

Before computing either metric, both the gold standard and the prediction are normalised
using the same function:

.. code-block:: python

   import re, unicodedata

   def normalize(text):
       text = unicodedata.normalize("NFKD", text)
       text = text.lower()
       text = text.replace("ſ", "s")     # long s → regular s
       text = text.replace("œ", "oe")
       text = text.replace("æ", "ae")
       text = re.sub(r"[.,;:!?()\[\]\"'&]", " ", text)
       text = re.sub(r"\s+", " ", text)
       return text.strip()

This ensures that differences in punctuation or Unicode encoding do not artificially
inflate error rates.