API Reference
=============

run_mistral_ocr(image_path)
---------------------------
Extract text from an image using Mistral OCR API.

clean_markdown(text)
--------------------
Removes markdown artifacts and normalizes text.

run_mistral_correction(text)
----------------------------
Uses Mistral Large to correct OCR errors.

normalize(text)
---------------
Prepares text for evaluation (lowercase, remove punctuation).

cer(gold, pred)
---------------
Computes Character Error Rate.

wer(gold, pred)
---------------
Computes Word Error Rate.