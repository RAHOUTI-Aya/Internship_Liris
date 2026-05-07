import re
import unicodedata
from ollama import chat

# CONFIG

IMAGE_PATH = "page_13.png"

GOLD_PATH = "page_13.txt"

OUTPUT_PATH = "qwen_pipeline_results_page_13.txt"

OCR_MODEL = "qwen2.5vl:7b"
LLM_MODEL = "qwen2.5vl:7b"

# ÉTAPE 1 : QWEN OCR

def run_qwen_ocr(image_path: str) -> str:

    print("[1/4] Qwen OCR en cours...")

    response = chat(
        model=OCR_MODEL,
        messages=[
            {
                "role": "user",
                "content": (
                    "Transcribe this historical French document exactly as written. "
                    "Preserve archaic spelling, punctuation, capitalization, "
                    "and line order. Do not summarize."
                ),
                "images": [image_path]
            }
        ]
    )

    text = response["message"]["content"].strip()

    print(f"    → {len(text)} caractères extraits")

    return text


# ÉTAPE 2 : NETTOYAGE

def clean_text(text: str) -> str:

    print("[2/4] Nettoyage du texte...")

    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    print(f"    → {len(text)} caractères après nettoyage")

    return text


# ÉTAPE 3 : POST-CORRECTION LLM

def run_qwen_correction(ocr_text: str) -> str:

    print("[3/4] Correction LLM en cours...")

    system_prompt = """
You are an expert in 18th century French historical texts and OCR correction.

Your task:
- Correct ONLY obvious OCR mistakes.
- Preserve historical spelling and archaic French.
- Preserve historical punctuation and capitalization.
- Do NOT modernize the language.

Examples to preserve:
- étoit
- appelloit
- portoient
- avoit
- passans

Correct:
- broken OCR words
- obvious letter confusions
- corrupted characters
- split words

Output rules:
- Return ONLY the corrected text.
- No explanations.
- No comments.
"""

    response = chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": ocr_text
            }
        ]
    )

    corrected = response["message"]["content"].strip()

    corrected = re.sub(r"\n+", " ", corrected)
    corrected = re.sub(r"\s+", " ", corrected)

    print(f"    → {len(corrected)} caractères après correction")

    return corrected


# ÉTAPE 4 : NORMALISATION

def normalize(text: str) -> str:

    text = unicodedata.normalize("NFKD", text)

    text = text.lower()

    text = text.replace("\n", " ")

    text = text.replace("ſ", "s")

    text = text.replace("œ", "oe")
    text = text.replace("æ", "ae")

    text = re.sub(r"[.,;:!?()\[\]\"'&]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# LEVENSHTEIN

def levenshtein_chars(a: str, b: str) -> int:

    n, m = len(a), len(b)

    dp = list(range(m + 1))

    for i in range(1, n + 1):

        prev = dp[:]

        dp[0] = i

        for j in range(1, m + 1):

            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[j] = min(
                dp[j] + 1,
                dp[j - 1] + 1,
                prev[j - 1] + cost
            )

    return dp[m]


def levenshtein_words(a: list, b: list) -> int:

    n, m = len(a), len(b)

    dp = list(range(m + 1))

    for i in range(1, n + 1):

        prev = dp[:]

        dp[0] = i

        for j in range(1, m + 1):

            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[j] = min(
                dp[j] + 1,
                dp[j - 1] + 1,
                prev[j - 1] + cost
            )

    return dp[m]


# CER / WER

def cer(gold: str, pred: str) -> float:

    return levenshtein_chars(gold, pred) / max(len(gold), 1)


def wer(gold: str, pred: str) -> float:

    g = gold.split()
    p = pred.split()

    return levenshtein_words(g, p) / max(len(g), 1)


# PIPELINE PRINCIPAL

def main():

    print("=" * 60)
    print("PIPELINE : Qwen OCR + Qwen LLM correction")
    print("=" * 60)

    # GOLD Standard

    with open(GOLD_PATH, "r", encoding="utf-8") as f:

        gold_raw = f.read()

    gold_raw = re.sub(r"\n+", " ", gold_raw)
    gold_raw = re.sub(r"\s+", " ", gold_raw).strip()

    print(f"Gold Standard chargé : {len(gold_raw)} caractères\n")

    # OCR

    ocr_raw = run_qwen_ocr(IMAGE_PATH)

    # CLEAN

    ocr_clean = clean_text(ocr_raw)

    # CORRECTION

    corrected = run_qwen_correction(ocr_clean)

    # NORMALIZATION

    print("[4/4] Évaluation en cours...")

    gold_norm = normalize(gold_raw)

    ocr_norm = normalize(ocr_clean)

    corr_norm = normalize(corrected)

    # METRICS

    cer_ocr = cer(gold_norm, ocr_norm)
    wer_ocr = wer(gold_norm, ocr_norm)

    cer_corr = cer(gold_norm, corr_norm)
    wer_corr = wer(gold_norm, corr_norm)



    report = f"""
============================================================
PIPELINE : Qwen OCR + Qwen correction
============================================================

--- Qwen OCR seul ---
CER : {cer_ocr:.4f}
WER : {wer_ocr:.4f}

--- Qwen OCR + correction ---
CER : {cer_corr:.4f}
WER : {wer_corr:.4f}

--- Gain ---
ΔCER : {cer_ocr - cer_corr:+.4f}
ΔWER : {wer_ocr - wer_corr:+.4f}

============================================================
TEXTES
============================================================

[GOLD STANDARD]
{gold_raw}

[OCR BRUT QWEN]
{ocr_clean}

[APRÈS CORRECTION]
{corrected}
"""

    print(report)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:

        f.write(report)

    print(f"\nRésultats sauvegardés dans : {OUTPUT_PATH}")




if __name__ == "__main__":

    main()