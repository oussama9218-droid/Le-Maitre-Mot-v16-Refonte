# Statut des générateurs par chapitre - Collège (6e → 3e)

## Légende
- ✅ **Générateur dédié** : Énoncé pédagogique structuré, `is_fallback: false`
- ⚠️ **Fallback** : Énoncé généré automatiquement (moins précis), `is_fallback: true`
- ❌ **Non mappé** : Chapitre non disponible dans l'API V1

---

## 🔴 VAGUE 1 - Implémentés (2024-12-11)

### Références Google Sheet "LeMaitreMot-6e"
- Vue Synthétique : Ligne X
- Spécifications Algorithmiques : Ligne Y
- Énoncés Modèles : Section Z

| Famille | Code Ref | Chapitre API | generator_code | Statut |
|---------|----------|--------------|----------------|--------|
| Représentation graphique fractions | `6N2-FRAC-REPR` | Fractions | `6e_FRACTION_REPRESENTATION` | ✅ |
| Tableaux de proportionnalité | `6N3-PROP-TAB` | Proportionnalité | `6e_PROP_TABLEAU` | ✅ |
| Problèmes d'achats | `6N3-PROP-ACHAT` | Proportionnalité | `6e_PROP_ACHAT` | ✅ |
| Problèmes 2 étapes | `6P-PROB-2ET` | Géométrie dans le plan | `6e_PROBLEME_2_ETAPES` | ✅ |
| Lecture/écriture nombres | `6N1-LECTURE` | Nombres entiers et décimaux | `6e_NOMBRES_LECTURE` | ✅ |
| Comparaison/rangement nombres | `6N1-COMP` | Nombres entiers et décimaux | `6e_NOMBRES_COMPARAISON` | ✅ |

### Générateurs déjà existants (avant Vague 1)

| Famille | Chapitre API | generator_code | Statut |
|---------|--------------|----------------|--------|
| Addition/soustraction fractions | Fractions | `6e_CALCUL_FRACTIONS` | ✅ |
| Symétrique point | Symétrie axiale | `6e_SYMETRIE_AXIALE` | ✅ |
| Symétrique figure | Symétrie axiale | `6e_SYMETRIE_AXIALE` | ✅ |
| Tableau proportionnalité (legacy) | Proportionnalité | `6e_PROPORTIONNALITE` | ✅ |
| Périmètre/aire rectangle | Périmètres et aires | `6e_PERIMETRE_AIRE` | ✅ |

---

## 6e - Mathématiques (Détail complet)

### Nombres et calculs

| Chapitre | Types disponibles | Statut |
|----------|-------------------|--------|
| Nombres entiers et décimaux | `CALCUL_DECIMAUX`, `NOMBRES_LECTURE`, `NOMBRES_COMPARAISON` | ✅ 3 types |
| Fractions | `CALCUL_FRACTIONS`, `FRACTION_REPRESENTATION` | ✅ 2 types |
| Nombres en écriture fractionnaire | `CALCUL_FRACTIONS` | ✅ |

### Proportionnalité

| Chapitre | Types disponibles | Statut |
|----------|-------------------|--------|
| Proportionnalité | `PROPORTIONNALITE`, `PROP_TABLEAU`, `PROP_ACHAT` | ✅ 3 types |

### Géométrie

| Chapitre | Types disponibles | Statut |
|----------|-------------------|--------|
| Symétrie axiale | `SYMETRIE_AXIALE` | ✅ |
| Périmètres et aires | `PERIMETRE_AIRE`, `RECTANGLE` | ✅ |
| Géométrie dans le plan | `RECTANGLE`, `TRIANGLE_QUELCONQUE`, `PROBLEME_2_ETAPES` | ✅ |

---

## 🟠 VAGUE 2 - À implémenter (Priorité Haute)

| Famille | Code Ref | Complexité | SVG |
|---------|----------|------------|-----|
| Droite graduée (entiers) | `6N1-DROITE` | Moyenne | ✅ |
| Droite graduée (décimaux) | `6N2-DROITE` | Moyenne | ✅ |
| Fraction sur droite graduée | `6N2-FRAC-DROITE` | Moyenne | ✅ |
| Comparaison fractions | `6N2-FRAC-COMP` | Simple | Non |
| Coefficient multiplicateur | `6N3-PROP-COEFF` | Simple | Non |
| Vitesse/durée/distance | `6N3-VDD` | Simple | Non |
| Aire triangle | `6G1-AIRE-TRI` | Moyenne | ✅ |
| Figures composées | `6G1-AIRE-COMP` | Lourde | ✅ |
| Volume pavé droit | `6G3-VOL-PAVE` | Simple | Non |
| Lire tableau | `6D-TAB-LIRE` | Simple | Non |
| Diagramme en barres | `6D-DIAG-BAR` | Moyenne | ✅ |
| Problème 1 étape | `6P-PROB-1ET` | Simple | Non |
| Triangle | `6G-TRI` | Simple | ✅ |
| Quadrilatères | `6G-QUAD` | Simple | ✅ |
| Mesure angle | `6G-ANGLE` | Moyenne | ✅ |
| Formules | `6L-FORM` | Simple | Non |

---

## 🟡 VAGUE 3 - À implémenter (Priorité Moyenne)

- Décomposition nombres
- Encadrement
- Arrondi/troncature
- Fractions égales
- Graphiques proportionnalité
- Priorités opératoires
- Parenthèses
- Erreurs courantes
- Critères divisibilité
- Multiples
- Conversions unités
- Propriétés symétrie
- Compléter tableau
- Diagramme circulaire
- Substitution simple
- Vocabulaire angles
- Propriétés angles
- Cercle

---

*Mis à jour le : 2024-12-11 - Vague 1 complète*
