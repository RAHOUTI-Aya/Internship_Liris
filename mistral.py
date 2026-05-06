import base64
import requests
import re
import unicodedata


MISTRAL_API_KEY = "..."

IMAGE_PATH = "page_1905.png"
GOLD_PATH  = "page_1905.txt"
OUTPUT_PATH = "evaluation_results.txt"

# Step 1 : MISTRAL OCR


def run_mistral_ocr(image_path: str) -> str:
    print("Mistral OCR")
    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        "https://api.mistral.ai/v1/ocr",
        headers={
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral-ocr-latest",
            "document": {
                "type": "image_url",
                "image_url": f"data:image/png;base64,{base64_image}"
            }
        }
    )
    result = response.json()

    if "pages" not in result:
        raise ValueError(f"Mistral OCR Error: {result}")

    raw = "\n".join(page["markdown"] for page in result["pages"])
    print(f"    → {len(raw)} caractères extraits")
    return raw


# Step 2 : Markdown Cleaning

def clean_markdown(text: str) -> str:
    print("Nettoyage du markdown")
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)          # supprimer images
    text = re.sub(r"#{1,6}\s*", "", text)                 # supprimer titres
    text = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", text)   # supprimer gras/italique
    text = re.sub(r"_{1,2}(.*?)_{1,2}", r"\1", text)     # supprimer soulignement
    text = re.sub(r"&amp;", "&", text)                    # décoder &amp;
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)            # supprimer liens
    text = re.sub(r"`{1,3}.*?`{1,3}", "", text)          # supprimer code inline
    text = re.sub(r"\n+", " ", text)                      # tout en une ligne
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    print(f"    → {len(text)} caractères après nettoyage")
    return text


# Step 3 : MISTRAL LARGE POST-CORRECTION

def run_mistral_correction(ocr_text: str) -> str:
    print(" Mistral Large post-correction")

    system_prompt = """Tu es un expert en paléographie et en textes juridiques français du XVIIIe siècle (Dictionnaire de Trévoux, 1743).
Tu reçois une transcription OCR d'une page de dictionnaire et tu corriges UNIQUEMENT les erreurs manifestes.

RÈGLES ABSOLUES :
1. Conserver l'orthographe ancienne intentionnelle :
   - "portoient" (pas "portaient")
   - "batême" (pas "baptême") 
   - "plûpart" (pas "plupart")
   - "appelloit" (pas "appelait")
   - "payoient" (pas "payaient")
   - "transportoit" (pas "transportait")
   - "tenoient" (pas "tenaient")
   - "passans" (pas "passants")
   - "marchandises" avec orthographe d'époque

2. Corriger les erreurs OCR évidentes :
   - Accents parasites : "Genereès" → "Generès"
   - Confusion de lettres : "Vestigal" → "Vectigal"
   - Mots coupés en fin de ligne : reconstituer le mot complet
   - "ſ" long = "s" normal

3. Corriger les substitutions sémantiques :
   - "entre deux foires" → "entre deux soleils"
   - "droit débile sans titre" → "droit établi sans titre"
   - "billote, ou branclerie" → "billette, ou branchière"
   - "barrange" → "barrage"
   - "caufel" → "casuel"
   - "préſté" → "prévôté"
   - "pour leurs privilèges" → "pour leurs provisions"

4. Corriger les noms propres :
   - "Bouleons" → "Boileau"
   - "Genili" → "Generoso"
   - "Péquire" → "Péguire"

5. Corriger les dates médiévales :
   - 1587 → 1387
   - 1688 → 1388

6. FORMAT DE SORTIE :
   - Texte en UNE SEULE LIGNE CONTINUE
   - Aucun retour à la ligne
   - Aucun commentaire
   - Aucune explication
   - UNIQUEMENT le texte corrigé"""

    user_prompt = f"""Corrige les erreurs OCR de ce texte extrait du Dictionnaire de Trévoux (1743).
Retourne UNIQUEMENT le texte corrigé en une seule ligne continue, sans aucun commentaire.

TEXTE OCR À CORRIGER :
{ocr_text}"""

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral-large-latest",
            "temperature": 0,
            "max_tokens": 4096,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ]
        }
    )

    result = response.json()
    if "choices" not in result:
        raise ValueError(f"Erreur Mistral Large : {result}")

    corrected = result["choices"][0]["message"]["content"].strip()
    corrected = re.sub(r"\n+", " ", corrected)
    corrected = re.sub(r"\s+", " ", corrected)
    print(f"    → {len(corrected)} caractères après correction")
    return corrected


# Step 4 : Normalization for Evaluation

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


# Step 5 : Metrics WER / CER

def levenshtein_chars(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev = dp[:]
        dp[0] = i
        for j in range(1, m + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[j] = min(dp[j] + 1, dp[j-1] + 1, prev[j-1] + cost)
    return dp[m]

def levenshtein_words(a: list, b: list) -> int:
    n, m = len(a), len(b)
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev = dp[:]
        dp[0] = i
        for j in range(1, m + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[j] = min(dp[j] + 1, dp[j-1] + 1, prev[j-1] + cost)
    return dp[m]

def cer(gold: str, pred: str) -> float:
    return levenshtein_chars(gold, pred) / max(len(gold), 1)

def wer(gold: str, pred: str) -> float:
    g, p = gold.split(), pred.split()
    return levenshtein_words(g, p) / max(len(g), 1)


# PIPELINE 

def main():

    # Lecture gold standard
    with open(GOLD_PATH, "r", encoding="utf-8") as f:
        gold_raw = f.read()
    gold_raw = re.sub(r"\n+", " ", gold_raw)
    gold_raw = re.sub(r"\s+", " ", gold_raw).strip()
    print(f"Gold chargé : {len(gold_raw)} caractères\n")

    #  1 : OCR
    ocr_raw   = run_mistral_ocr(IMAGE_PATH)

    #  2 : Nettoyage
    ocr_clean = clean_markdown(ocr_raw)

    #  3 : Correction
    corrected = run_mistral_correction(ocr_clean)

    #  4 : Normalisation
    gold_norm = normalize(gold_raw)
    ocr_norm  = normalize(ocr_clean)
    corr_norm = normalize(corrected)

    # Scores
    cer_ocr  = cer(gold_norm, ocr_norm)
    wer_ocr  = wer(gold_norm, ocr_norm)
    cer_corr = cer(gold_norm, corr_norm)
    wer_corr = wer(gold_norm, corr_norm)

    # Rapport de résultats
    report = f"""{'='*60}
PIPELINE : Mistral OCR + Mistral Large post-correction
{'='*60}

1-  Mistral OCR seul :
CER : {cer_ocr:.4f}
WER : {wer_ocr:.4f}

2-  Mistral OCR + Mistral Large :
CER : {cer_corr:.4f}
WER : {wer_corr:.4f}

3-  Gain apporté par la correction :
ΔCER : {cer_ocr - cer_corr:+.4f}
ΔWER : {wer_ocr - wer_corr:+.4f}

{'='*60}
TEXTES
{'='*60}

[GOLD STANDARD]
{gold_raw}

[OCR BRUT MISTRAL]
{ocr_clean}

[APRÈS CORRECTION MISTRAL LARGE]
{corrected}
"""

    print("\n" + report)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nRésultats sauvegardés dans {OUTPUT_PATH}")


if __name__ == "__main__":
    main()