# Statut des générateurs par chapitre - 6ᵉ (Vagues 1, 2 & 3 complètes)

## Légende
- ✅ **Générateur dédié** : Énoncé pédagogique structuré, `is_fallback: false`
- 🆕 **Nouveau** : Ajouté dans cette session
- ⚠️ **Chapitre absent** : Générateur prêt mais chapitre non disponible dans le catalogue

---

## 📊 Statistiques

| Vague | Générateurs créés | Types disponibles |
|-------|-------------------|-------------------|
| Vague 1 | 6 | 6 |
| Vague 2 | 16 | 16 |
| Vague 3 | 13 | 13 |
| **Total** | **35** | **35** |

---

## Chapitres disponibles dans le catalogue 6ᵉ

### Nombres et calculs

| Chapitre | Types d'exercices | Statut |
|----------|-------------------|--------|
| Nombres entiers et décimaux | `CALCUL_DECIMAUX`, `NOMBRES_LECTURE`, `NOMBRES_COMPARAISON` | ✅ 3 types |
| Fractions | `CALCUL_FRACTIONS`, `FRACTION_REPRESENTATION` | ✅ 2 types |
| Nombres en écriture fractionnaire | `CALCUL_FRACTIONS` | ✅ |
| Calcul mental | `PRIORITES_OPERATIONS` | ✅ 🆕 |
| Longueurs, masses, durées | `CONVERSIONS_UNITES`, `CALCUL_DECIMAUX` | ✅ 🆕 |

### Proportionnalité

| Chapitre | Types d'exercices | Statut |
|----------|-------------------|--------|
| Proportionnalité | `PROPORTIONNALITE`, `PROP_TABLEAU`, `PROP_ACHAT` | ✅ 3 types |

### Géométrie

| Chapitre | Types d'exercices | Statut |
|----------|-------------------|--------|
| Symétrie axiale | `SYMETRIE_AXIALE`, `SYMETRIE_PROPRIETES` | ✅ 2 types 🆕 |
| Périmètres et aires | `PERIMETRE_AIRE`, `RECTANGLE`, `AIRE_TRIANGLE`, `AIRE_FIGURES_COMPOSEES` | ✅ 4 types 🆕 |
| Aires | `PERIMETRE_AIRE`, `AIRE_TRIANGLE`, `CERCLE` | ✅ 3 types 🆕 |
| Volumes | `VOLUME_PAVE`, `VOLUME` | ✅ 2 types 🆕 |
| Angles | `ANGLE_MESURE`, `ANGLE_VOCABULAIRE`, `ANGLE_PROPRIETES` | ✅ 3 types 🆕 |
| Géométrie dans le plan | `RECTANGLE`, `TRIANGLE_QUELCONQUE`, `PROBLEME_2_ETAPES`, `TRIANGLE_CONSTRUCTION`, `QUADRILATERES` | ✅ 5 types 🆕 |
| Géométrie dans l'espace | `VOLUME` | ✅ |

---

## Générateurs créés (prêts mais nécessitant ajout au catalogue)

Ces générateurs sont implémentés et fonctionnels, mais les chapitres correspondants n'existent pas encore dans le catalogue. Ils seront disponibles dès que les chapitres seront ajoutés.

| Code | Générateur | Description |
|------|------------|-------------|
| 6N1-DROITE | `DROITE_GRADUEE_ENTIERS` | Droite graduée avec entiers |
| 6N2-DROITE | `DROITE_GRADUEE_DECIMAUX` | Droite graduée avec décimaux |
| 6N2-FRAC-DROITE | `FRACTION_DROITE` | Fractions sur droite graduée |
| 6N2-FRAC-COMP | `FRACTION_COMPARAISON` | Comparaison de fractions |
| 6N2-FRAC-EG | `FRACTIONS_EGALES` | Fractions égales et simplification |
| 6N3-PROP-COEFF | `PROP_COEFFICIENT` | Coefficient de proportionnalité |
| 6N3-VDD | `VITESSE_DUREE_DISTANCE` | Vitesse, durée, distance |
| 6D-TAB-LIRE | `TABLEAU_LECTURE` | Lecture de tableaux |
| 6D-TAB-COMP | `TABLEAU_COMPLETER` | Compléter un tableau |
| 6D-DIAG-BAR | `DIAGRAMME_BARRES` | Diagrammes en barres |
| 6D-DIAG-CIRC | `DIAGRAMME_CIRCULAIRE` | Diagrammes circulaires |
| 6P-PROB-1ET | `PROBLEME_1_ETAPE` | Problèmes à 1 étape |
| 6G-TRI | `TRIANGLE_CONSTRUCTION` | Construction de triangles |
| 6G-QUAD | `QUADRILATERES` | Propriétés des quadrilatères |
| 6L-FORM | `FORMULES` | Utilisation de formules |
| 6L-SUBST | `SUBSTITUTION` | Substitution dans expressions |
| 6N-DECOMP | `DECOMPOSITION` | Décomposition des nombres |
| 6N-ENCAD | `ENCADREMENT` | Encadrement de nombres |
| 6N-ARRONDI | `ARRONDI` | Arrondi de nombres |
| 6C-PRIO | `PRIORITES_OPERATIONS` | Priorités opératoires |
| 6N-DIV | `CRITERES_DIVISIBILITE` | Critères de divisibilité |
| 6N-MULT | `MULTIPLES` | Multiples d'un nombre |
| 6M-CONV | `CONVERSIONS_UNITES` | Conversions d'unités |

---

## Liste complète des générateurs par code

### Vague 1 (Priorité Très Haute) ✅
| Code | Type | Fonction |
|------|------|----------|
| 6N2-FRAC-REPR | `FRACTION_REPRESENTATION` | `_gen_fraction_representation` |
| 6N3-PROP-TAB | `PROP_TABLEAU` | `_gen_prop_tableau` |
| 6N3-PROP-ACHAT | `PROP_ACHAT` | `_gen_prop_achat` |
| 6P-PROB-2ET | `PROBLEME_2_ETAPES` | `_gen_probleme_2_etapes` |
| 6N1-LECTURE | `NOMBRES_LECTURE` | `_gen_nombres_lecture` |
| 6N1-COMP | `NOMBRES_COMPARAISON` | `_gen_nombres_comparaison` |

### Vague 2 (Priorité Haute) ✅
| Code | Type | Fonction |
|------|------|----------|
| 6N1-DROITE | `DROITE_GRADUEE_ENTIERS` | `_gen_droite_graduee_entiers` |
| 6N2-DROITE | `DROITE_GRADUEE_DECIMAUX` | `_gen_droite_graduee_decimaux` |
| 6N2-FRAC-DROITE | `FRACTION_DROITE` | `_gen_fraction_droite` |
| 6N2-FRAC-COMP | `FRACTION_COMPARAISON` | `_gen_fraction_comparaison` |
| 6N3-PROP-COEFF | `PROP_COEFFICIENT` | `_gen_prop_coefficient` |
| 6N3-VDD | `VITESSE_DUREE_DISTANCE` | `_gen_vitesse_duree_distance` |
| 6G1-AIRE-TRI | `AIRE_TRIANGLE` | `_gen_aire_triangle` |
| 6G1-AIRE-COMP | `AIRE_FIGURES_COMPOSEES` | `_gen_aire_figures_composees` |
| 6G3-VOL-PAVE | `VOLUME_PAVE` | `_gen_volume_pave` |
| 6D-TAB-LIRE | `TABLEAU_LECTURE` | `_gen_tableau_lecture` |
| 6D-DIAG-BAR | `DIAGRAMME_BARRES` | `_gen_diagramme_barres` |
| 6P-PROB-1ET | `PROBLEME_1_ETAPE` | `_gen_probleme_1_etape` |
| 6G-TRI | `TRIANGLE_CONSTRUCTION` | `_gen_triangle_construction` |
| 6G-QUAD | `QUADRILATERES` | `_gen_quadrilateres` |
| 6G-ANGLE | `ANGLE_MESURE` | `_gen_angle_mesure` |
| 6L-FORM | `FORMULES` | `_gen_formules` |

### Vague 3 (Priorité Moyenne) ✅
| Code | Type | Fonction |
|------|------|----------|
| 6N2-FRAC-EG | `FRACTIONS_EGALES` | `_gen_fractions_egales` |
| 6N-DECOMP | `DECOMPOSITION` | `_gen_decomposition` |
| 6N-ENCAD | `ENCADREMENT` | `_gen_encadrement` |
| 6N-ARRONDI | `ARRONDI` | `_gen_arrondi` |
| 6C-PRIO | `PRIORITES_OPERATIONS` | `_gen_priorites_operations` |
| 6N-DIV | `CRITERES_DIVISIBILITE` | `_gen_criteres_divisibilite` |
| 6N-MULT | `MULTIPLES` | `_gen_multiples` |
| 6M-CONV | `CONVERSIONS_UNITES` | `_gen_conversions_unites` |
| 6G-ANG-VOC | `ANGLE_VOCABULAIRE` | `_gen_angle_vocabulaire` |
| 6G-ANG-PROP | `ANGLE_PROPRIETES` | `_gen_angle_proprietes` |
| 6G-SYM-PROP | `SYMETRIE_PROPRIETES` | `_gen_symetrie_proprietes` |
| 6D-TAB-COMP | `TABLEAU_COMPLETER` | `_gen_tableau_completer` |
| 6D-DIAG-CIRC | `DIAGRAMME_CIRCULAIRE` | `_gen_diagramme_circulaire` |
| 6L-SUBST | `SUBSTITUTION` | `_gen_substitution` |

---

*Mis à jour le : 2024-12-11 - Vagues 1, 2 & 3 complètes*
