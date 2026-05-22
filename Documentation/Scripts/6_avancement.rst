Pipeline OCR — Dictionnaire de Trévoux
========================================

.. contents:: Table des matières
   :depth: 2
   :local:

Présentation
------------

Ce projet est un pipeline d'évaluation OCR développé dans le cadre d'un stage de recherche.
L'objectif est de comparer différents moteurs OCR sur les pages numérisées du
**Dictionnaire de Trévoux** (1743), un dictionnaire encyclopédique français du XVIIIe siècle
imprimé en deux colonnes, en caractères anciens incluant le long-s (ſ), des ligatures et
une orthographe historique.

Le pipeline permet de lancer un moteur OCR sur une image, de comparer la sortie à un
gold standard, de corriger automatiquement les erreurs via un LLM, et d'évaluer les
résultats avec les métriques CER et WER.

----

Architecture du projet
-----------------------

.. code-block:: text

   ocr_pipelineV2/
   ├── app.py                  # Serveur Flask principal — interface OCR + comparaison
   ├── app1.py                 # Interface CER / WER Calculator (port 5001)
   ├── requirements.txt
   ├── ocr/
   │   └── engines.py          # Wrappers des moteurs OCR
   ├── evaluation/
   │   └── metrics.py          # Calcul WER, CER, diff mot-à-mot
   ├── data/
   │   ├── images/             # Pages scannées (.png, .jpg)
   │   ├── gold/               # Gold standards (fichiers .txt)
   │   └── results/            # Résultats JSON et CSV
   └── templates/
       └── index.html          # Interface web principale

----

Moteurs OCR testés
-------------------

Quatre moteurs ont été intégrés et testés sur le corpus.

Kraken + CATMuS-Print Large ★
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Moteur recommandé pour ce corpus. Le modèle `CATMuS-Print Large
<https://zenodo.org/record/10592716>`_ est entraîné spécifiquement sur des imprimés
historiques français et latins (XVe–XIXe siècle).

- Gestion native du long-s (ſ), des ligatures et de l'orthographe d'époque
- **WER : ~8 %**, **CER : ~1,8 %** sur les pages testées
- Modèle téléchargé via ``kraken get 10.5281/zenodo.10592716``
- Fichier : ``catmus-print-fondue-large.mlmodel``

.. code-block:: bash

   kraken -i page.png output.txt segment -bl ocr -m catmus-print-fondue-large.mlmodel

Tesseract 5
~~~~~~~~~~~

Moteur généraliste open-source. Moins performant sur le vieux français sans modèle
spécialisé. Langues testées : ``fra``, ``lat``, ``fra+lat``.

EasyOCR
~~~~~~~

Moteur basé sur un réseau de neurones profond. Simple à installer, mais pas optimisé
pour les caractères historiques.

Surya
~~~~~

Moteur récent basé sur des transformers. Produit une sortie JSON structurée
(``text_lines``, ``confidence``, coordonnées polygonales par caractère et par mot).
Performant sur le texte moderne, moins adapté au long-s et aux ligatures historiques.

----

Problème identifié : lecture en colonnes
-----------------------------------------

Le Dictionnaire de Trévoux est imprimé sur **deux colonnes par page**. La plupart des
moteurs OCR lisent les lignes horizontalement en traversant les deux colonnes, ce qui
produit un texte entrelacé incohérent.

Exemple de sortie Surya désalignée :

.. code-block:: text

   étoit fortifié par une triple muraille, & par trois forteresses; nord.
   mais ni ses fortifications [...] SYRIE PROPRE. C'est la partie...

Le mot ``nord.`` appartient à la colonne de droite mais s'insère au milieu de la
phrase de gauche. Ce problème structural est distinct des erreurs OCR classiques et
impacte fortement les métriques (WER > 80 % malgré une reconnaissance correcte des
caractères).

Confusion long-s / f
~~~~~~~~~~~~~~~~~~~~~

Le long-s (ſ) est fréquemment confondu avec le ``f`` ou le ``s`` selon le moteur :

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Gold standard
     - Sortie OCR
     - Erreur
   * - ``sont``
     - ``font``
     - long-s lu comme f
   * - ``selon``
     - ``felon``
     - long-s lu comme f
   * - ``ses``
     - ``fes``
     - long-s lu comme f
   * - ``femme``
     - ``semme``
     - f initial lu comme long-s
   * - ``sauva``
     - ``fauva``
     - long-s lu comme f

----

Correction LLM
--------------

Un module de correction post-OCR via LLM a été intégré. L'API Groq est utilisée
(accès gratuit) avec le modèle **Llama 3.3 70B**.

Stratégies de prompt disponibles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Diplomatique complet (recommandé)**
   Prompt few-shot avec exemples de corrections typiques du Trévoux.
   Règles explicites : long-s, accents manquants, orthographe d'époque conservée (``étoit``,
   ``avoit``, ``&``), pas de modernisation.

**Diplomatique court**
   Version allégée pour les modèles à faible limite de tokens.

**Zero-shot simple**
   Prompt minimal, sans exemples.

Modèles testés via Groq
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Modèle
     - Taille
     - Statut
   * - ``llama-3.3-70b-versatile`` ★
     - 70B
     - Actif
   * - ``llama-3.3-8b-versatile``
     - 8B
     - Actif (tokens limités)
   * - ``llama3-70b-8192``
     - 70B
     - Actif
   * - ``mixtral-8x7b-32768``
     - 8x7B
     - **Décommissionné**
   * - ``gemma2-9b-it``
     - 9B
     - **Décommissionné**

----

Évaluation : CER et WER
------------------------

Deux métriques sont calculées par alignement de séquences (distance de Levenshtein).

.. glossary::

   CER (Character Error Rate)
      Taux d'erreur au niveau du caractère.
      ``CER = (substitutions + insertions + suppressions) / nombre de caractères de référence``

   WER (Word Error Rate)
      Taux d'erreur au niveau du mot.
      ``WER = (substitutions + insertions + suppressions) / nombre de mots de référence``

Résultats sur la page de test (p1905)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 20 20

   * - Moteur
     - CER
     - WER
   * - Kraken + CATMuS-Print Large ★
     - ~1,8 %
     - ~8 %
   * - Surya (sans correction layout)
     - élevé
     - > 80 %
   * - Tesseract 5 (fra+lat)
     - élevé
     - élevé

.. note::

   Le WER élevé de Surya est principalement causé par le problème de lecture en
   colonnes (texte entrelacé), et non par des erreurs de reconnaissance de caractères.

----

Interfaces web
--------------

app.py — Interface principale (port 5000)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $env:PYTHONUTF8=1   # Windows PowerShell
   python app.py
   # -> http://localhost:5000

Fonctionnalités :

- Upload d'une image de page
- Sélection du moteur OCR (Kraken+CATMuS, Tesseract, EasyOCR, Surya)
- Saisie du gold standard
- Lancement de l'OCR et affichage du texte brut
- Correction automatique via LLM (Groq)
- Affichage des métriques CER / WER
- Diff coloré mot à mot (rouge = erreur, vert = correction)

app1.py — CER / WER Calculator (port 5001)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python app1.py
   # -> http://localhost:5001

Interface légère autonome. Permet de coller directement un gold standard et un texte
OCR pour calculer CER et WER sans passer par le pipeline complet.
Utile pour évaluer des sorties externes (ex. : fichier JSON Surya converti en texte brut).

----

Installation
------------

.. code-block:: bash

   cd ocr_pipelineV2
   python -m venv .venv

   # Windows
   .venv\Scripts\Activate.ps1

   pip install flask flask-cors pillow numpy tqdm groq
   pip install pytesseract easyocr

   # Kraken + modèle CATMuS
   pip install kraken
   kraken get 10.5281/zenodo.10592716

Variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Windows PowerShell — évite les erreurs d'encodage Unicode
   $env:PYTHONUTF8=1

   # Clé API Groq (correction LLM)
   $env:GROQ_API_KEY="votre_cle"

----

Prochaines étapes
-----------------

- Intégrer une détection automatique de colonnes (segmentation layout) avant l'OCR
- Tester d'autres modèles Kraken spécialisés (CATMuS-Medieval, etc.)
- Construire un gold standard annoté sur un plus grand nombre de pages
- Comparer les stratégies de prompt LLM sur un jeu d'évaluation contrôlé
- Explorer l'API Mistral comme alternative à Groq