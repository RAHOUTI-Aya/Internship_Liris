Remarques 
==============================

Difficultés récurrentes relevées sur le corpus. Elles motivent le schéma
d'annotation du layout (voir :doc:`7_finetuning`) et guident la définition des
règles d'annotation.


Vedette secondaire ou expression ?
----------------------------------

.. figure:: /Documentation/Images/Vedette-sec-ou-non.png
   :width: 100%
   :align: center
   :alt: Article PUITS — ambiguïté vedette secondaire / expression
   :name: vedette-sec

   Article *PUITS* : faut-il annoter « Le PUITS de celui qui vit & me voit »
   et « PÉNÉTRER DANS LE PUITS DE DÉMOCRITE » comme ``Vedette-secondaire`` ?

Les expressions et locutions à l'intérieur d'un article sont composées dans la
**même petite capitale** que les vraies sous-entrées. Visuellement, rien ne les
distingue d'une ``Vedette-secondaire``. À l'inverse, ``PULA``, ``PULCHERIA`` et
``PULEGIUM`` sont de vraies nouvelles entrées (``Mot-vedette``), et « PUL. » est
un ``Section-lexicale``.

**Conséquence** : règle d'annotation à fixer — une expression citée dans le
corps n'est pas une vedette. Critère retenu : une ``Vedette-secondaire`` ouvre
une définition propre, l'expression reste rattachée au sens de la vedette
principale.


Opérations arithmétiques intégrées
----------------------------------

.. figure:: /Documentation/Images/operations_soustraction.png
   :width: 100%
   :align: center
   :alt: Article SOUSTRACTION — blocs de chiffres
   :name: soustraction

   Article *SOUSTRACTION* : exemples de soustractions posées, en blocs de
   chiffres dans la colonne de droite.

Les opérations posées (chiffres empilés et alignés) sont structurellement des
**tableaux** insérés dans le texte courant. L'OCR mélange les chiffres et perd
l'alignement vertical ; ces zones doivent être isolées en ``Tableau`` pour être
traitées à part (et non lues comme du texte linéaire).

On note aussi des ``Manicule`` (☞) en marge de ``SOUS-TIRAGE`` et
``SOUS-TIRER``, à détecter comme zones propres.


Initiale détachée de la vedette (p. 931)
----------------------------------------

.. figure:: /Documentation/Images/Pb_p931.png
   :width: 100%
   :align: center
   :alt: Page 931 — initiale R détachée des vedettes RENGIER et RENGORGER
   :name: p931

   Page 931 : l'initiale « R » de ``RENGIER`` et ``RENGORGER`` est rejetée
   seule en début de ligne.

La capitale initiale est typographiquement détachée du reste du mot. La
segmentation la lit comme un élément isolé : la vedette est **scindée** en
« R » + « ENGIER », ce qui casse l'identification du ``Mot-vedette``.

**Piste** : regrouper l'initiale isolée avec la suite de la vedette lors du
post-traitement, ou annoter la zone vedette complète pour le fine-tuning layout.


Première lettre tronquée
------------------------

.. figure:: /Documentation/Images/S_missing.png
   :width: 100%
   :align: center
   :alt: Vedette SYMPHITUM lue YMPHITUM, S initial manquant
   :name: s-missing

   La vedette ``SYMPHITUM`` est lue « YMPHITUM » : le « S » initial est perdu.

La première lettre de la vedette est coupée au **bord de la zone** (crop de
colonne trop serré ou polygone de ligne démarrant trop à droite). Le mot-clé
d'entrée devient erroné, ce qui est critique pour l'indexation.


Autres remarques: 
------------------------

Différence résultats OCR entre les pages :


- Exemple 1:

.. figure:: /Documentation/Images/Ile1.png
   :width: 100%
   :align: center
   

.. figure:: /Documentation/Images/Ile2.png
   :width: 100%
   :align: center
   

- Exemple 2:


.. figure:: /Documentation/Images/Lieu1.png
   :width: 100%
   :align: center


.. figure:: /Documentation/Images/Lieu2.png
   :width: 100%
   :align: center


- Exemple 3:

.. figure:: /Documentation/Images/pecher1.png
   :width: 100%
   :align: center
   

.. figure:: /Documentation/Images/pecher2.png
   :width: 100%
   :align: center


