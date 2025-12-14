# Test Results - GM08 Chapitre Pilote #2

## Feature: 6e_GM08 - Grandeurs et mesures (Longueurs, Périmètres)

### Backend Tests to Run:
1. **Endpoint batch GM08** - POST `/api/v1/exercises/generate/batch/gm08`
   - Test avec `offer: "free"` et différentes difficultés
   - Test avec `offer: "pro"` pour accéder aux 20 exercices
   - Vérifier unicité des exercices (zéro doublon)
   - Vérifier le warning quand pool < demandé

2. **Endpoint single GM08** - POST `/api/v1/exercises/generate`
   - Test avec `code_officiel: "6e_GM08"`
   - Vérifier filtrage par difficulté et offer

3. **Contenu des exercices**
   - HTML pur (pas de LaTeX/Markdown)
   - Solution en 4 étapes
   - Familles: CONVERSION, COMPARAISON, PERIMETRE, PROBLEME

### Frontend Tests to Run:
1. **Page /generate**
   - Sélectionner "Longueurs, masses, durées" en mode simple
   - Passer en mode "Officiel" et chercher GM08
   - Générer des exercices GM08
   - Vérifier l'affichage des exercices

2. **Variation**
   - Cliquer sur "Variation" doit générer de nouveaux exercices GM08

### Test Data:
- FREE: 10 exercices (ids 1-10)
- PRO: 10 exercices supplémentaires (ids 11-20)
- Difficultés: facile (6), moyen (7), difficile (7)

### API URL:
`https://exerrchive.preview.emergentagent.com/api/v1/exercises`
