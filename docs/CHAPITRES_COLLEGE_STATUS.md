# Statut des générateurs par chapitre - 6ᵉ (Audit Complet)

> **Dernière mise à jour** : Audit automatisé réussi ✅
> **Résultat** : 15/15 chapitres mappés et fonctionnels

---

## 📊 Statistiques Globales

| Métrique | Valeur |
|----------|--------|
| **Types d'exercices (enum)** | 62 |
| **Méthodes générateurs** | 72 |
| **Chapitres 6ᵉ mappés** | 15/15 ✅ |

### Répartition par Vague

| Vague | Générateurs créés | Description |
|-------|-------------------|-------------|
| Vague 1 | 6 | Fractions, Proportionnalité, Nombres |
| Vague 2 | 16 | Droites graduées, Aires, Volumes, Tableaux |
| Vague 3 | 13 | Encadrement, Priorités, Divisibilité, Symétrie |
| **Total** | **35** | Générateurs dédiés 6ᵉ |

---

## ✅ Chapitres 6ᵉ - Mapping Complet

### Nombres et calculs

| Chapitre | Types d'exercices | Statut |
|----------|-------------------|--------|
| Nombres entiers et décimaux | `CALCUL_DECIMAUX`, `NOMBRES_LECTURE`, `NOMBRES_COMPARAISON` | ✅ 3 types |
| Fractions | `CALCUL_FRACTIONS`, `FRACTION_REPRESENTATION` | ✅ 2 types |
| Nombres en écriture fractionnaire | `CALCUL_FRACTIONS` | ✅ 1 type |
| Calcul mental | `PRIORITES_OPERATIONS`, `CALCUL_DECIMAUX` | ✅ 2 types |
| Calculs posés | `CALCUL_DECIMAUX`, `CALCUL_FRACTIONS` | ✅ 2 types |
| Calculs instrumentés | `CALCUL_DECIMAUX`, `CONVERSIONS_UNITES` | ✅ 2 types |

### Grandeurs et mesures

| Chapitre | Types d'exercices | Statut |
|----------|-------------------|--------|
| Longueurs, masses, durées | `CONVERSIONS_UNITES`, `CALCUL_DECIMAUX` | ✅ 2 types |
| Aires | `PERIMETRE_AIRE`, `AIRE_TRIANGLE`, `CERCLE` | ✅ 3 types |
| Périmètres et aires | `PERIMETRE_AIRE`, `RECTANGLE`, `AIRE_TRIANGLE`, `AIRE_FIGURES_COMPOSEES` | ✅ 4 types |
| Volumes | `VOLUME` | ✅ 1 type |
| Angles | `ANGLE_MESURE`, `ANGLE_VOCABULAIRE`, `ANGLE_PROPRIETES` | ✅ 3 types |

### Espace et géométrie

| Chapitre | Types d'exercices | Statut |
|----------|-------------------|--------|
| Géométrie dans l'espace | `VOLUME` | ✅ 1 type |
| Géométrie dans le plan | `RECTANGLE`, `TRIANGLE_QUELCONQUE`, `PROBLEME_2_ETAPES`, `TRIANGLE_CONSTRUCTION`, `QUADRILATERES` | ✅ 5 types |
| Symétrie axiale | `SYMETRIE_AXIALE`, `SYMETRIE_PROPRIETES` | ✅ 2 types |

### Organisation et gestion de données

| Chapitre | Types d'exercices | Statut |
|----------|-------------------|--------|
| Proportionnalité | `PROPORTIONNALITE`, `PROP_TABLEAU`, `PROP_ACHAT` | ✅ 3 types |

---

## 📋 Liste complète des générateurs par code

### Vague 1 (Priorité Très Haute) ✅

| Code | Type (enum) | Fonction | Description |
|------|-------------|----------|-------------|
| 6N2-FRAC-REPR | `FRACTION_REPRESENTATION` | `_gen_fraction_representation` | Représentation graphique de fractions |
| 6N3-PROP-TAB | `PROP_TABLEAU` | `_gen_prop_tableau` | Tableaux de proportionnalité |
| 6N3-PROP-ACHAT | `PROP_ACHAT` | `_gen_prop_achat` | Problèmes d'achat proportionnels |
| 6P-PROB-2ET | `PROBLEME_2_ETAPES` | `_gen_probleme_2_etapes` | Problèmes à 2 étapes |
| 6N1-LECTURE | `NOMBRES_LECTURE` | `_gen_nombres_lecture` | Lecture/écriture de nombres |
| 6N1-COMP | `NOMBRES_COMPARAISON` | `_gen_nombres_comparaison` | Comparaison de nombres |

### Vague 2 (Priorité Haute) ✅

| Code | Type (enum) | Fonction | Description |
|------|-------------|----------|-------------|
| 6N1-DROITE | `DROITE_GRADUEE_ENTIERS` | `_gen_droite_graduee_entiers` | Droite graduée avec entiers |
| 6N2-DROITE | `DROITE_GRADUEE_DECIMAUX` | `_gen_droite_graduee_decimaux` | Droite graduée avec décimaux |
| 6N2-FRAC-DROITE | `FRACTION_DROITE` | `_gen_fraction_droite` | Fractions sur droite graduée |
| 6N2-FRAC-COMP | `FRACTION_COMPARAISON` | `_gen_fraction_comparaison` | Comparaison de fractions |
| 6N3-PROP-COEFF | `PROP_COEFFICIENT` | `_gen_prop_coefficient` | Coefficient de proportionnalité |
| 6N3-VDD | `VITESSE_DUREE_DISTANCE` | `_gen_vitesse_duree_distance` | Vitesse, durée, distance |
| 6G1-AIRE-TRI | `AIRE_TRIANGLE` | `_gen_aire_triangle` | Aire de triangles |
| 6G1-AIRE-COMP | `AIRE_FIGURES_COMPOSEES` | `_gen_aire_figures_composees` | Aire de figures composées |
| 6G3-VOL-PAVE | `VOLUME_PAVE` | `_gen_volume_pave` | Volume de pavés droits |
| 6D-TAB-LIRE | `TABLEAU_LECTURE` | `_gen_tableau_lecture` | Lecture de tableaux |
| 6D-DIAG-BAR | `DIAGRAMME_BARRES` | `_gen_diagramme_barres` | Diagrammes en barres |
| 6P-PROB-1ET | `PROBLEME_1_ETAPE` | `_gen_probleme_1_etape` | Problèmes à 1 étape |
| 6G-TRI | `TRIANGLE_CONSTRUCTION` | `_gen_triangle_construction` | Construction de triangles |
| 6G-QUAD | `QUADRILATERES` | `_gen_quadrilateres` | Propriétés des quadrilatères |
| 6G-ANGLE | `ANGLE_MESURE` | `_gen_angle_mesure` | Mesure d'angles |
| 6L-FORM | `FORMULES` | `_gen_formules` | Utilisation de formules |

### Vague 3 (Priorité Moyenne) ✅

| Code | Type (enum) | Fonction | Description |
|------|-------------|----------|-------------|
| 6N2-FRAC-EG | `FRACTIONS_EGALES` | `_gen_fractions_egales` | Fractions égales et simplification |
| 6N-DECOMP | `DECOMPOSITION` | `_gen_decomposition` | Décomposition des nombres |
| 6N-ENCAD | `ENCADREMENT` | `_gen_encadrement` | Encadrement de nombres |
| 6N-ARRONDI | `ARRONDI` | `_gen_arrondi` | Arrondi de nombres |
| 6C-PRIO | `PRIORITES_OPERATIONS` | `_gen_priorites_operations` | Priorités opératoires |
| 6N-DIV | `CRITERES_DIVISIBILITE` | `_gen_criteres_divisibilite` | Critères de divisibilité |
| 6N-MULT | `MULTIPLES` | `_gen_multiples` | Multiples d'un nombre |
| 6M-CONV | `CONVERSIONS_UNITES` | `_gen_conversions_unites` | Conversions d'unités |
| 6G-ANG-VOC | `ANGLE_VOCABULAIRE` | `_gen_angle_vocabulaire` | Vocabulaire des angles |
| 6G-ANG-PROP | `ANGLE_PROPRIETES` | `_gen_angle_proprietes` | Propriétés des angles |
| 6G-SYM-PROP | `SYMETRIE_PROPRIETES` | `_gen_symetrie_proprietes` | Propriétés de la symétrie |
| 6D-TAB-COMP | `TABLEAU_COMPLETER` | `_gen_tableau_completer` | Compléter un tableau |
| 6D-DIAG-CIRC | `DIAGRAMME_CIRCULAIRE` | `_gen_diagramme_circulaire` | Diagrammes circulaires |
| 6L-SUBST | `SUBSTITUTION` | `_gen_substitution` | Substitution dans expressions |

---

## 📋 Générateurs spécifiques par chapitre (Sprint 1-4)

Ces générateurs sont mappés directement à des chapitres spécifiques via `chapter_specific_generators` :

| Chapitre | Fonction dédiée |
|----------|-----------------|
| Perpendiculaires et parallèles à la règle et à l'équerre | `_gen_perpendiculaires_paralleles` |
| Droite numérique et repérage | `_gen_droite_numerique` |
| Lire et compléter des tableaux de données | `_gen_tableaux_donnees` |
| Points, segments, droites, demi-droites | `_gen_points_segments_droites` |
| Alignement, milieu d'un segment | `_gen_alignement_milieu` |
| Lire et écrire les nombres entiers | `_gen_lire_ecrire_entiers` |
| Comparer et ranger des nombres entiers | `_gen_comparer_ranger_entiers` |
| Addition et soustraction de nombres entiers | `_gen_addition_soustraction_entiers` |
| Triangles (construction et classification) | `_gen_triangles` |
| Quadrilatères usuels | `_gen_quadrilateres` |
| Multiplication de nombres entiers | `_gen_multiplication_entiers` |
| Division euclidienne | `_gen_division_euclidienne` |
| Multiples et diviseurs, critères de divisibilité | `_gen_multiples_diviseurs` |
| Fractions comme partage et quotient | `_gen_fractions_partage` |
| Fractions simples de l'unité | `_gen_fractions_simples` |
| Mesurer et comparer des longueurs | `_gen_mesurer_longueurs` |
| Périmètre de figures usuelles | `_gen_perimetre_figures` |
| Aire du rectangle et du carré | `_gen_aire_rectangle_carre` |
| Diagrammes en barres et pictogrammes | `_gen_diagrammes_barres` |

---

## 📋 Générateurs génériques (multi-niveaux)

Ces générateurs sont utilisés par plusieurs chapitres et niveaux :

| Type | Fonction | Chapitres concernés |
|------|----------|---------------------|
| `CALCUL_RELATIFS` | `_gen_calcul_relatifs` | Nombres relatifs (5e+) |
| `CALCUL_FRACTIONS` | `_gen_calcul_fractions` | Fractions (tous niveaux) |
| `CALCUL_DECIMAUX` | `_gen_calcul_decimaux` | Décimaux, Calculs posés |
| `EQUATION_1ER_DEGRE` | `_gen_equation_1er_degre` | Équations (4e+) |
| `TRIANGLE_RECTANGLE` | `_gen_triangle_rectangle` | Pythagore (4e+) |
| `TRIANGLE_QUELCONQUE` | `_gen_triangle_quelconque` | Géométrie plane |
| `RECTANGLE` | `_gen_rectangle` | Aires, Périmètres |
| `CERCLE` | `_gen_cercle` | Cercle, Aires |
| `PERIMETRE_AIRE` | `_gen_perimetre_aire` | Périmètres et aires |
| `VOLUME` | `_gen_volume` | Volumes (tous niveaux) |
| `STATISTIQUES` | `_gen_statistiques` | Statistiques |
| `PROBABILITES` | `_gen_probabilites` | Probabilités (3e+) |
| `PUISSANCES` | `_gen_puissances` | Puissances (4e+) |
| `THALES` | `_gen_thales` | Théorème de Thalès (3e) |
| `TRIGONOMETRIE` | `_gen_trigonometrie` | Trigonométrie (3e) |
| `SYMETRIE_AXIALE` | `_gen_symetrie_axiale` | Symétrie axiale |
| `SYMETRIE_CENTRALE` | `_gen_symetrie_centrale` | Symétrie centrale (5e) |
| `PROPORTIONNALITE` | `_gen_proportionnalite` | Proportionnalité |

---

## 🔄 Prochaines étapes

### À faire (Validation pédagogique)
- [ ] Validation par l'utilisateur des énoncés générés pour chaque chapitre
- [ ] Test des niveaux de difficulté (facile/moyen/difficile)
- [ ] Vérification des formulations pédagogiques

### Améliorations futures
- [ ] Export PDF V1 pour la page `/generate`
- [ ] Ajout de nouveaux chapitres au catalogue UI
- [ ] Refactoring de `math_generation_service.py` (fichier volumineux)

---

*Document généré automatiquement par script d'audit*
