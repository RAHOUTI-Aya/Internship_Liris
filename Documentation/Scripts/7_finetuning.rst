Fine-tuning des modèles
=======================

Trois fine-tunings ont été explorés pour adapter le pipeline à la typographie
particulière du *Dictionnaire de Trévoux* (1743) : la reconnaissance de texte
(CATMuS), la segmentation de lignes (blla) et la détection de mise en page
(DocLayout-YOLO). Les annotations ont été réalisées sur un sous-ensemble du
corpus (956 pages extraites à 300 DPI via PyMuPDF).

.. contents::
   :local:
   :depth: 1


Reconnaissance — CATMuS-Print Large (eScriptorium)
--------------------------------------------------

Objectif : adapter le modèle de reconnaissance ``CATMuS-Print Large`` aux
caractères et ligatures propres au Trévoux.

- **Environnement** : eScriptorium (annotation + entraînement Kraken).
- **Données** : 12 pages transcrites ligne à ligne (vérité de terrain).
- **Modèle de base** : ``CATMuS-Print Large``.
- **Résultat** : précision de validation **~98,5 %** à l'epoch 12.

.. note::

   La précision est mesurée au niveau de la ligne sur le jeu de validation
   d'eScriptorium. Un jeu de test indépendant reste à construire pour confirmer
   le gain en conditions réelles (CER / WER sur pages non vues).


Segmentation de lignes — blla (eScriptorium)
--------------------------------------------

Objectif : améliorer la détection des lignes de base (*baselines*) par
fine-tuning du modèle de segmentation ``blla``.

- **Environnement** : eScriptorium.
- **Modèle produit** : ``blla-line-seg-ft35.mlmodel`` (5,05 Mo).

Le modèle fine-tuné n'a **pas** dépassé le ``blla`` par défaut. Comparaison des
configurations :

.. list-table::
   :header-rows: 1
   :widths: 50 15 35

   * - Configuration
     - CER
     - Remarque
   * - DocLayout-YOLO (colonnes) + ``blla`` par défaut
     - ~2,1 %
     - Pipeline retenu (page ``page_0948``)
   * - ``blla`` fine-tuné, image entière
     - ~7,3 %
     - Lignes correctes mais inférieur au défaut
   * - ``blla`` fine-tuné, sur crops de colonnes
     - ~57,5 %
     - Doublon de lecture (texte lu deux fois)

.. note::

   Appliqué directement aux crops de colonnes produits par DocLayout-YOLO, le
   modèle fine-tuné re-segmentait des zones déjà découpées, provoquant une
   double lecture du texte (CER ~57,5 %). Sur l'image entière le problème
   disparaît, mais le résultat reste en deçà du ``blla`` par défaut.

**Décision** : conserver la configuration par défaut **DocLayout-YOLO
(colonnes) + blla (lignes)** pour la production. CER ~2,1 % sur pages propres,
~19–20 % sur les pages difficiles près de la reliure.


Mise en page — DocLayout-YOLO (Label Studio)
--------------------------------------------

Objectif : fine-tuner DocLayout-YOLO pour la séparation des colonnes et la
détection fine des zones logiques de l'article de dictionnaire.

- **Outil d'annotation** : Label Studio.
- **Schéma d'annotation** : défini avec l'encadrement, plus riche qu'une simple
  distinction texte/colonne.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Label
     - Description
   * - ``Mot-vedette``
     - Entrée principale (tête d'article)
   * - ``Vedette-secondaire``
     - Sous-entrée / renvoi en petites capitales
   * - ``Paragraphe``
     - Corps de texte
   * - ``Paragraphe-suite``
     - Continuation d'un paragraphe (changement de colonne / page)
   * - ``Citation``
     - Citation ou exemple
   * - ``Section-lexicale``
     - Marqueur alphabétique (ex. « PUL. »)
   * - ``Manicule``
     - Main pointée (☞)
   * - ``Lettrine``
     - Initiale ornée
   * - ``Illustration``
     - Figure / gravure
   * - ``Titre``
     - Titre de section
   * - ``Autre-paratexte``
     - En-têtes courants (``PEC``, ``ASC``, ``SYM``), numéros de page
   * - ``Tableau``
     - Contenu tabulaire ou numérique

**État** : interface d'annotation Label Studio configurée ; annotation et
entraînement en cours. Les cas ambigus rencontrés lors de l'annotation sont
documentés dans :doc:`8_remarques`.
