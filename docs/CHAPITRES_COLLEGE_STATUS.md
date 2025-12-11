# 📚 Générateurs 6ᵉ - Documentation V1 Finale

> **Version** : V1 Finale  
> **Date** : Décembre 2024  
> **Statut** : ✅ Tous les chapitres opérationnels

---

## 📊 Statistiques Globales

| Métrique | Valeur |
|----------|--------|
| **Chapitres 6ᵉ** | 15 |
| **Types d'exercices mappés** | 42 |
| **Minimum par chapitre** | 2 types ✅ |
| **Maximum par chapitre** | 5 types |
| **Méthodes _gen_*** | 72 |

---

## ✅ Mapping Complet Chapitre → Générateurs

### 📐 Nombres et calculs (6 chapitres)

| Chapitre | Types d'exercices | Nb | Statut |
|----------|-------------------|:--:|:------:|
| **Nombres entiers et décimaux** | `CALCUL_DECIMAUX`, `NOMBRES_LECTURE`, `NOMBRES_COMPARAISON` | 3 | ✅ |
| **Fractions** | `CALCUL_FRACTIONS`, `FRACTION_REPRESENTATION`, `FRACTION_COMPARAISON` | 3 | ✅ |
| **Nombres en écriture fractionnaire** | `CALCUL_FRACTIONS`, `FRACTIONS_EGALES`, `FRACTION_COMPARAISON` | 3 | ✅ |
| **Calcul mental** | `PRIORITES_OPERATIONS`, `CALCUL_DECIMAUX` | 2 | ✅ |
| **Calculs posés** | `CALCUL_DECIMAUX`, `CALCUL_FRACTIONS` | 2 | ✅ |
| **Calculs instrumentés** | `CALCUL_DECIMAUX`, `CONVERSIONS_UNITES` | 2 | ✅ |

### 📏 Grandeurs et mesures (5 chapitres)

| Chapitre | Types d'exercices | Nb | Statut |
|----------|-------------------|:--:|:------:|
| **Longueurs, masses, durées** | `CONVERSIONS_UNITES`, `CALCUL_DECIMAUX` | 2 | ✅ |
| **Aires** | `PERIMETRE_AIRE`, `AIRE_TRIANGLE`, `CERCLE` | 3 | ✅ |
| **Périmètres et aires** | `PERIMETRE_AIRE`, `RECTANGLE`, `AIRE_TRIANGLE`, `AIRE_FIGURES_COMPOSEES` | 4 | ✅ |
| **Volumes** | `VOLUME_PAVE`, `VOLUME`, `CONVERSIONS_UNITES` | 3 | ✅ |
| **Angles** | `ANGLE_MESURE`, `ANGLE_VOCABULAIRE`, `ANGLE_PROPRIETES` | 3 | ✅ |

### 🔷 Espace et géométrie (3 chapitres)

| Chapitre | Types d'exercices | Nb | Statut |
|----------|-------------------|:--:|:------:|
| **Géométrie dans l'espace** | `VOLUME_PAVE`, `VOLUME` | 2 | ✅ |
| **Géométrie dans le plan** | `RECTANGLE`, `TRIANGLE_QUELCONQUE`, `PROBLEME_2_ETAPES`, `TRIANGLE_CONSTRUCTION`, `QUADRILATERES` | 5 | ✅ |
| **Symétrie axiale** | `SYMETRIE_AXIALE`, `SYMETRIE_PROPRIETES` | 2 | ✅ |

### 📊 Organisation et gestion de données (1 chapitre)

| Chapitre | Types d'exercices | Nb | Statut |
|----------|-------------------|:--:|:------:|
| **Proportionnalité** | `PROPORTIONNALITE`, `PROP_TABLEAU`, `PROP_ACHAT` | 3 | ✅ |

---

## 📋 Liste Complète des Générateurs par Code

### Vague 1 - Priorité Très Haute ✅

| Code | Type (enum) | Fonction | Description | Statut |
|------|-------------|----------|-------------|:------:|
| 6N2-FRAC-REPR | `FRACTION_REPRESENTATION` | `_gen_fraction_representation` | Représentation graphique de fractions | ✅ |
| 6N3-PROP-TAB | `PROP_TABLEAU` | `_gen_prop_tableau` | Tableaux de proportionnalité | ✅ |
| 6N3-PROP-ACHAT | `PROP_ACHAT` | `_gen_prop_achat` | Problèmes d'achat proportionnels | ✅ |
| 6P-PROB-2ET | `PROBLEME_2_ETAPES` | `_gen_probleme_2_etapes` | Problèmes à 2 étapes | ✅ |
| 6N1-LECTURE | `NOMBRES_LECTURE` | `_gen_nombres_lecture` | Lecture/écriture de nombres | ✅ |
| 6N1-COMP | `NOMBRES_COMPARAISON` | `_gen_nombres_comparaison` | Comparaison de nombres | ✅ |

### Vague 2 - Priorité Haute ✅

| Code | Type (enum) | Fonction | Description | Statut |
|------|-------------|----------|-------------|:------:|
| 6N1-DROITE | `DROITE_GRADUEE_ENTIERS` | `_gen_droite_graduee_entiers` | Droite graduée avec entiers | ✅ |
| 6N2-DROITE | `DROITE_GRADUEE_DECIMAUX` | `_gen_droite_graduee_decimaux` | Droite graduée avec décimaux | ✅ |
| 6N2-FRAC-DROITE | `FRACTION_DROITE` | `_gen_fraction_droite` | Fractions sur droite graduée | ✅ |
| 6N2-FRAC-COMP | `FRACTION_COMPARAISON` | `_gen_fraction_comparaison` | Comparaison de fractions | ✅ |
| 6N3-PROP-COEFF | `PROP_COEFFICIENT` | `_gen_prop_coefficient` | Coefficient de proportionnalité | ✅ |
| 6N3-VDD | `VITESSE_DUREE_DISTANCE` | `_gen_vitesse_duree_distance` | Vitesse, durée, distance | ✅ |
| 6G1-AIRE-TRI | `AIRE_TRIANGLE` | `_gen_aire_triangle` | Aire de triangles | ✅ |
| 6G1-AIRE-COMP | `AIRE_FIGURES_COMPOSEES` | `_gen_aire_figures_composees` | Aire de figures composées | ✅ |
| 6G3-VOL-PAVE | `VOLUME_PAVE` | `_gen_volume_pave` | Volume de pavés droits | ✅ |
| 6D-TAB-LIRE | `TABLEAU_LECTURE` | `_gen_tableau_lecture` | Lecture de tableaux | ✅ |
| 6D-DIAG-BAR | `DIAGRAMME_BARRES` | `_gen_diagramme_barres` | Diagrammes en barres | ✅ |
| 6P-PROB-1ET | `PROBLEME_1_ETAPE` | `_gen_probleme_1_etape` | Problèmes à 1 étape | ✅ |
| 6G-TRI | `TRIANGLE_CONSTRUCTION` | `_gen_triangle_construction` | Construction de triangles | ✅ |
| 6G-QUAD | `QUADRILATERES` | `_gen_quadrilateres` | Propriétés des quadrilatères | ✅ |
| 6G-ANGLE | `ANGLE_MESURE` | `_gen_angle_mesure` | Mesure d'angles | ✅ |
| 6L-FORM | `FORMULES` | `_gen_formules` | Utilisation de formules | ✅ |

### Vague 3 - Priorité Moyenne ✅

| Code | Type (enum) | Fonction | Description | Statut |
|------|-------------|----------|-------------|:------:|
| 6N2-FRAC-EG | `FRACTIONS_EGALES` | `_gen_fractions_egales` | Fractions égales et simplification | ✅ |
| 6N-DECOMP | `DECOMPOSITION` | `_gen_decomposition` | Décomposition des nombres | ✅ |
| 6N-ENCAD | `ENCADREMENT` | `_gen_encadrement` | Encadrement de nombres | ✅ |
| 6N-ARRONDI | `ARRONDI` | `_gen_arrondi` | Arrondi de nombres | ✅ |
| 6C-PRIO | `PRIORITES_OPERATIONS` | `_gen_priorites_operations` | Priorités opératoires | ✅ |
| 6N-DIV | `CRITERES_DIVISIBILITE` | `_gen_criteres_divisibilite` | Critères de divisibilité | ✅ |
| 6N-MULT | `MULTIPLES` | `_gen_multiples` | Multiples d'un nombre | ✅ |
| 6M-CONV | `CONVERSIONS_UNITES` | `_gen_conversions_unites` | Conversions d'unités | ✅ |
| 6G-ANG-VOC | `ANGLE_VOCABULAIRE` | `_gen_angle_vocabulaire` | Vocabulaire des angles | ✅ |
| 6G-ANG-PROP | `ANGLE_PROPRIETES` | `_gen_angle_proprietes` | Propriétés des angles | ✅ |
| 6G-SYM-PROP | `SYMETRIE_PROPRIETES` | `_gen_symetrie_proprietes` | Propriétés de la symétrie | ✅ |
| 6D-TAB-COMP | `TABLEAU_COMPLETER` | `_gen_tableau_completer` | Compléter un tableau | ✅ |
| 6D-DIAG-CIRC | `DIAGRAMME_CIRCULAIRE` | `_gen_diagramme_circulaire` | Diagrammes circulaires | ✅ |
| 6L-SUBST | `SUBSTITUTION` | `_gen_substitution` | Substitution dans expressions | ✅ |

---

## 📋 Générateurs Spécifiques par Chapitre (Sprint 1-4)

Ces générateurs sont mappés directement à des chapitres spécifiques via `chapter_specific_generators` :

| Chapitre | Fonction | Statut |
|----------|----------|:------:|
| Perpendiculaires et parallèles... | `_gen_perpendiculaires_paralleles` | ✅ |
| Droite numérique et repérage | `_gen_droite_numerique` | ✅ |
| Lire et compléter des tableaux... | `_gen_tableaux_donnees` | ✅ |
| Points, segments, droites... | `_gen_points_segments_droites` | ✅ |
| Alignement, milieu d'un segment | `_gen_alignement_milieu` | ✅ |
| Lire et écrire les nombres entiers | `_gen_lire_ecrire_entiers` | ✅ |
| Comparer et ranger des nombres... | `_gen_comparer_ranger_entiers` | ✅ |
| Addition et soustraction... | `_gen_addition_soustraction_entiers` | ✅ |
| Triangles (construction...) | `_gen_triangles` | ✅ |
| Quadrilatères usuels | `_gen_quadrilateres` | ✅ |
| Multiplication de nombres entiers | `_gen_multiplication_entiers` | ✅ |
| Division euclidienne | `_gen_division_euclidienne` | ✅ |
| Multiples et diviseurs... | `_gen_multiples_diviseurs` | ✅ |
| Fractions comme partage... | `_gen_fractions_partage` | ✅ |
| Fractions simples de l'unité | `_gen_fractions_simples` | ✅ |
| Mesurer et comparer des longueurs | `_gen_mesurer_longueurs` | ✅ |
| Périmètre de figures usuelles | `_gen_perimetre_figures` | ✅ |
| Aire du rectangle et du carré | `_gen_aire_rectangle_carre` | ✅ |
| Diagrammes en barres... | `_gen_diagrammes_barres` | ✅ |

---

## 📋 Générateurs Génériques (Multi-niveaux)

| Type | Fonction | Niveaux |
|------|----------|---------|
| `CALCUL_RELATIFS` | `_gen_calcul_relatifs` | 5e+ |
| `CALCUL_FRACTIONS` | `_gen_calcul_fractions` | 6e+ |
| `CALCUL_DECIMAUX` | `_gen_calcul_decimaux` | 6e+ |
| `EQUATION_1ER_DEGRE` | `_gen_equation_1er_degre` | 4e+ |
| `TRIANGLE_RECTANGLE` | `_gen_triangle_rectangle` | 4e+ |
| `TRIANGLE_QUELCONQUE` | `_gen_triangle_quelconque` | 6e+ |
| `RECTANGLE` | `_gen_rectangle` | 6e+ |
| `CERCLE` | `_gen_cercle` | 6e+ |
| `PERIMETRE_AIRE` | `_gen_perimetre_aire` | 6e+ |
| `VOLUME` | `_gen_volume` | 6e+ |
| `STATISTIQUES` | `_gen_statistiques` | 6e+ |
| `PROBABILITES` | `_gen_probabilites` | 3e+ |
| `PUISSANCES` | `_gen_puissances` | 4e+ |
| `THALES` | `_gen_thales` | 3e |
| `TRIGONOMETRIE` | `_gen_trigonometrie` | 3e+ |
| `SYMETRIE_AXIALE` | `_gen_symetrie_axiale` | 6e+ |
| `SYMETRIE_CENTRALE` | `_gen_symetrie_centrale` | 5e+ |
| `PROPORTIONNALITE` | `_gen_proportionnalite` | 6e+ |

---

## 🔧 Architecture Technique

### Structure JSON de sortie (API `/api/v1/exercises/generate`)

```json
{
  "id_exercice": "ex_6e_fractions_123456789",
  "niveau": "6e",
  "chapitre": "Fractions",
  "enonce_html": "<div class='exercise-enonce'>...</div>",
  "svg": null | "<svg>...</svg>",
  "solution_html": "<div class='exercise-solution'>...</div>",
  "pdf_token": "ex_6e_fractions_123456789",
  "metadata": {
    "type_exercice": "standard",
    "difficulte": "moyen",
    "duree_estimee": 5,
    "points": 2.0,
    "domaine": "Nombres et calculs",
    "has_figure": false,
    "is_fallback": false,
    "generator_code": "6e_FRACTION_REPRESENTATION"
  }
}
```

### Conventions d'énoncés

- **HTML** : Énoncés avec balises `<p>`, `<ol>`, `<table>`, etc.
- **LaTeX** : Formules mathématiques avec `$...$` ou `$$...$$`
- **SVG** : Figures géométriques générées dynamiquement

---

## 📝 Notes pour Validation Pédagogique

### Générateurs à valider en priorité (Beta)
- `_gen_diagramme_circulaire` - Vérifier les pourcentages
- `_gen_prop_graphique` - Vérifier la lecture graphique
- `_gen_symetrie_proprietes` - Vérifier les constructions

### Points d'attention
1. **Niveaux de difficulté** : Vérifier la cohérence facile/moyen/difficile
2. **Formulations** : Adapter le vocabulaire au niveau 6e
3. **Valeurs numériques** : S'assurer de résultats "propres" (entiers ou décimaux simples)

---

## 🔄 Prochaines Étapes

- [ ] Validation pédagogique complète par Perplexity
- [ ] Export PDF V1 pour `/generate`
- [ ] Implémentation du niveau 5e
- [ ] Refactoring de `math_generation_service.py`

---

*Document généré automatiquement - V1 Finale*
