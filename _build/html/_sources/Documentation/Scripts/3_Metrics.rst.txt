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