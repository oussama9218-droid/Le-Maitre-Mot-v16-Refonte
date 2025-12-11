"""
Service de génération d'exercices mathématiques structurés
Génère specs mathématiques complètes avec solutions calculées (SANS IA)
"""

import random
import math
from fractions import Fraction
from typing import List, Dict, Any, Tuple
import logging
from models.math_models import (
    MathExerciseSpec, MathExerciseType, DifficultyLevel, 
    GeometricFigure
)

logger = logging.getLogger(__name__)

class MathGenerationService:
    """Service de génération d'exercices mathématiques structurés"""
    
    def __init__(self):
        # Points utilisables pour la géométrie (éviter ABC en premier)
        self.geometry_points_sets = [
            ["D", "E", "F"],
            ["M", "N", "P"], 
            ["R", "S", "T"],
            ["X", "Y", "Z"],
            ["G", "H", "I"],
            ["U", "V", "W"],  # ✅ Remplace ["J", "K", "L"] pour éviter "L" (faux positif avec "L'")
            ["A", "B", "C"]  # Dernier recours
        ]
        self.used_points_sets = set()
    
    def generate_math_exercise_specs(
        self, 
        niveau: str, 
        chapitre: str, 
        difficulte: str, 
        nb_exercices: int
    ) -> List[MathExerciseSpec]:
        """Point d'entrée principal - génère les specs d'exercices"""
        
        # Reset pour chaque génération
        self.used_points_sets.clear()
        
        # Mapper chapitre vers types d'exercices
        exercise_types = self._map_chapter_to_types(chapitre, niveau)
        
        specs = []
        for i in range(nb_exercices):
            # Choisir un type d'exercice
            exercise_type = random.choice(exercise_types)
            
            # Générer la spec selon le type
            spec = self._generate_spec_by_type(
                niveau, chapitre, exercise_type, difficulte
            )
            
            if spec:
                specs.append(spec)
            
        return specs
    
    def _map_chapter_to_types(self, chapitre: str, niveau: str) -> List[MathExerciseType]:
        """Mappe les chapitres aux types d'exercices appropriés"""
        
        # Note: Les chapitres sont uniques dans le mapping
        # Pour des chapitres présents dans plusieurs niveaux, 
        # le mapping s'applique à tous les niveaux
        mapping = {
            # ========== 6e ==========
            "Nombres entiers et décimaux": [MathExerciseType.CALCUL_DECIMAUX],
            "Nombres décimaux": [MathExerciseType.CALCUL_DECIMAUX],
            "Longueurs, masses, durées": [MathExerciseType.CALCUL_DECIMAUX],
            "Périmètres et aires": [MathExerciseType.PERIMETRE_AIRE, MathExerciseType.RECTANGLE],
            "Aires": [MathExerciseType.PERIMETRE_AIRE, MathExerciseType.CERCLE],
            "Angles": [MathExerciseType.TRIANGLE_QUELCONQUE],  # Angles dans triangles
            "Géométrie - Triangles et quadrilatères": [MathExerciseType.RECTANGLE, MathExerciseType.PERIMETRE_AIRE],
            "Géométrie dans le plan": [MathExerciseType.RECTANGLE, MathExerciseType.TRIANGLE_QUELCONQUE],
            "Perpendiculaires et parallèles à la règle et à l'équerre": [MathExerciseType.TRIANGLE_QUELCONQUE, MathExerciseType.RECTANGLE],  # ✅ AJOUT PROMPT 5
            "Symétrie axiale": [MathExerciseType.SYMETRIE_AXIALE],  # ✅ Générateur symétrie axiale ajouté
            "Symétrie axiale (points, segments, figures)": [MathExerciseType.SYMETRIE_AXIALE],  # ✅ Titre complet de la migration
            "Symétrie centrale": [MathExerciseType.SYMETRIE_CENTRALE],  # ✅ Générateur symétrie centrale ajouté
            
            # ========== 6e - Nombres et calculs (SPRINT 1) ==========
            "Droite numérique et repérage": [MathExerciseType.CALCUL_DECIMAUX],
            
            # ========== 6e - Organisation et gestion de données (SPRINT 1) ==========
            "Lire et compléter des tableaux de données": [MathExerciseType.STATISTIQUES],
            
            # ========== 6e - Géométrie (SPRINT 2) ==========
            "Points, segments, droites, demi-droites": [MathExerciseType.TRIANGLE_QUELCONQUE],
            "Alignement, milieu d'un segment": [MathExerciseType.TRIANGLE_QUELCONQUE],
            
            # ========== 6e - Nombres et calculs (SPRINT 2) ==========
            "Lire et écrire les nombres entiers": [MathExerciseType.CALCUL_DECIMAUX],
            "Comparer et ranger des nombres entiers": [MathExerciseType.CALCUL_DECIMAUX],
            "Addition et soustraction de nombres entiers": [MathExerciseType.CALCUL_RELATIFS],
            
            # ========== 6e - Géométrie (SPRINT 3) ==========
            "Triangles (construction et classification)": [MathExerciseType.TRIANGLE_QUELCONQUE],
            "Quadrilatères usuels (carré, rectangle, losange, parallélogramme)": [MathExerciseType.RECTANGLE],
            
            # ========== 6e - Nombres et calculs (SPRINT 3) ==========
            "Multiplication de nombres entiers": [MathExerciseType.CALCUL_DECIMAUX],
            "Division euclidienne": [MathExerciseType.CALCUL_DECIMAUX],
            "Multiples et diviseurs, critères de divisibilité": [MathExerciseType.CALCUL_DECIMAUX],
            
            # ========== 6e - Fractions (SPRINT 4) ==========
            "Fractions comme partage et quotient": [MathExerciseType.CALCUL_FRACTIONS],
            "Fractions simples de l'unité": [MathExerciseType.CALCUL_FRACTIONS],
            "Nombres en écriture fractionnaire": [MathExerciseType.CALCUL_FRACTIONS],  # AJOUTÉ
            
            # ========== 6e - Grandeurs et mesures (SPRINT 4) ==========
            "Mesurer et comparer des longueurs": [MathExerciseType.CALCUL_DECIMAUX],
            "Périmètre de figures usuelles": [MathExerciseType.PERIMETRE_AIRE],
            "Aire du rectangle et du carré": [MathExerciseType.PERIMETRE_AIRE],
            
            # ========== 6e - Organisation et gestion de données (SPRINT 4) ==========
            "Diagrammes en barres et pictogrammes": [MathExerciseType.STATISTIQUES],
            
            # ========== Chapitres multi-niveaux (6e, 5e, 4e, 3e) ==========
            "Fractions": [MathExerciseType.CALCUL_FRACTIONS],
            "Proportionnalité": [MathExerciseType.PROPORTIONNALITE],
            "Nombres relatifs": [MathExerciseType.CALCUL_RELATIFS],
            "Nombres rationnels": [MathExerciseType.CALCUL_FRACTIONS],
            "Statistiques": [MathExerciseType.STATISTIQUES],
            "Géométrie dans l'espace": [MathExerciseType.VOLUME],
            "Volumes": [MathExerciseType.VOLUME],
            "Puissances": [MathExerciseType.PUISSANCES],
            "Calcul littéral": [MathExerciseType.EQUATION_1ER_DEGRE, MathExerciseType.CALCUL_DECIMAUX],
            
            # ========== 5e ==========
            "Triangles": [MathExerciseType.TRIANGLE_QUELCONQUE, MathExerciseType.TRIANGLE_RECTANGLE],
            "Aires et périmètres": [MathExerciseType.PERIMETRE_AIRE, MathExerciseType.CERCLE, MathExerciseType.RECTANGLE],
            "Angles et triangles": [MathExerciseType.TRIANGLE_QUELCONQUE],
            "Parallélogrammes": [MathExerciseType.RECTANGLE, MathExerciseType.PERIMETRE_AIRE],
            # ❌ "Symétrie centrale" RETIRÉ : Pas de générateur disponible
            # ❌ "Homothétie" RETIRÉ : Pas de générateur disponible
            
            # ========== 4e ==========
            "Théorème de Pythagore": [MathExerciseType.TRIANGLE_RECTANGLE],
            "Équations": [MathExerciseType.EQUATION_1ER_DEGRE],
            "Cosinus": [MathExerciseType.TRIGONOMETRIE],
            
            # ========== 3e et géométrie avancée ==========
            "Probabilités": [MathExerciseType.PROBABILITES],
            "Statistiques et probabilités": [MathExerciseType.STATISTIQUES, MathExerciseType.PROBABILITES],
            "Aires et volumes": [MathExerciseType.VOLUME, MathExerciseType.PERIMETRE_AIRE],
            "Théorème de Thalès": [MathExerciseType.THALES],
            "Trigonométrie": [MathExerciseType.TRIGONOMETRIE],
            "Le cercle": [MathExerciseType.CERCLE],
            "Cercle": [MathExerciseType.CERCLE],
            "Organisation et gestion de données, fonctions": [MathExerciseType.STATISTIQUES, MathExerciseType.PROPORTIONNALITE]
        }
        
        # 🚨 SÉCURITÉ CRITIQUE : Lever une erreur si chapitre inconnu
        if chapitre not in mapping:
            raise ValueError(
                f"❌ CHAPITRE NON MAPPÉ : '{chapitre}'\n"
                f"   Niveau : {niveau if 'niveau' in locals() else 'N/A'}\n"
                f"   Le chapitre existe dans le curriculum mais aucun générateur n'est défini.\n"
                f"   → Ajoutez ce chapitre au mapping dans _get_exercise_types_for_chapter()\n"
                f"   Chapitres disponibles : {sorted(mapping.keys())}"
            )
        
        return mapping[chapitre]
    
    def _generate_spec_by_type(
        self, 
        niveau: str, 
        chapitre: str, 
        exercise_type: MathExerciseType, 
        difficulte: str
    ) -> MathExerciseSpec:
        """Génère une spec selon le type d'exercice"""
        
        # SPRINT 1, 2 & 3 : Générateurs spécifiques par chapitre (priorité sur les types)
        chapter_specific_generators = {
            # SPRINT 1
            "Perpendiculaires et parallèles à la règle et à l'équerre": self._gen_perpendiculaires_paralleles,
            "Droite numérique et repérage": self._gen_droite_numerique,
            "Lire et compléter des tableaux de données": self._gen_tableaux_donnees,
            
            # SPRINT 2
            "Points, segments, droites, demi-droites": self._gen_points_segments_droites,
            "Alignement, milieu d'un segment": self._gen_alignement_milieu,
            "Lire et écrire les nombres entiers": self._gen_lire_ecrire_entiers,
            "Comparer et ranger des nombres entiers": self._gen_comparer_ranger_entiers,
            "Addition et soustraction de nombres entiers": self._gen_addition_soustraction_entiers,
            
            # SPRINT 3
            "Triangles (construction et classification)": self._gen_triangles,
            "Quadrilatères usuels (carré, rectangle, losange, parallélogramme)": self._gen_quadrilateres,
            "Multiplication de nombres entiers": self._gen_multiplication_entiers,
            "Division euclidienne": self._gen_division_euclidienne,
            "Multiples et diviseurs, critères de divisibilité": self._gen_multiples_diviseurs,
            
            # SPRINT 4
            "Fractions comme partage et quotient": self._gen_fractions_partage,
            "Fractions simples de l'unité": self._gen_fractions_simples,
            "Mesurer et comparer des longueurs": self._gen_mesurer_longueurs,
            "Périmètre de figures usuelles": self._gen_perimetre_figures,
            "Aire du rectangle et du carré": self._gen_aire_rectangle_carre,
            "Diagrammes en barres et pictogrammes": self._gen_diagrammes_barres,
        }
        
        # Vérifier si un générateur spécifique existe pour ce chapitre
        if chapitre in chapter_specific_generators:
            return chapter_specific_generators[chapitre](niveau, chapitre, difficulte)
        
        # Sinon, utiliser les générateurs par type d'exercice (système existant)
        generators = {
            MathExerciseType.CALCUL_RELATIFS: self._gen_calcul_relatifs,
            MathExerciseType.CALCUL_FRACTIONS: self._gen_calcul_fractions,
            MathExerciseType.CALCUL_DECIMAUX: self._gen_calcul_decimaux,
            MathExerciseType.EQUATION_1ER_DEGRE: self._gen_equation_1er_degre,
            MathExerciseType.TRIANGLE_RECTANGLE: self._gen_triangle_rectangle,
            MathExerciseType.TRIANGLE_QUELCONQUE: self._gen_triangle_quelconque,
            MathExerciseType.PROPORTIONNALITE: self._gen_proportionnalite,
            MathExerciseType.PERIMETRE_AIRE: self._gen_perimetre_aire,
            MathExerciseType.RECTANGLE: self._gen_rectangle,
            MathExerciseType.VOLUME: self._gen_volume,
            MathExerciseType.STATISTIQUES: self._gen_statistiques,
            MathExerciseType.PROBABILITES: self._gen_probabilites,
            MathExerciseType.PUISSANCES: self._gen_puissances,
            MathExerciseType.CERCLE: self._gen_cercle,
            MathExerciseType.THALES: self._gen_thales,
            MathExerciseType.TRIGONOMETRIE: self._gen_trigonometrie,
            MathExerciseType.SYMETRIE_AXIALE: self._gen_symetrie_axiale,
            MathExerciseType.SYMETRIE_CENTRALE: self._gen_symetrie_centrale
        }
        
        generator = generators.get(exercise_type)
        if generator:
            return generator(niveau, chapitre, difficulte)
        else:
            # Fallback
            return self._gen_calcul_decimaux(niveau, chapitre, difficulte)
    
    def _get_next_geometry_points(self) -> List[str]:
        """Retourne le prochain set de points géométriques non utilisé"""
        for point_set in self.geometry_points_sets:
            point_tuple = tuple(point_set)
            if point_tuple not in self.used_points_sets:
                self.used_points_sets.add(point_tuple)
                return point_set.copy()
        
        # Si tous utilisés, recommencer avec le premier
        self.used_points_sets.clear()
        self.used_points_sets.add(tuple(self.geometry_points_sets[0]))
        return self.geometry_points_sets[0].copy()
    
    
    def _are_points_aligned(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> bool:
        """
        Vérifie si trois points sont alignés
        Utilise le calcul de l'aire du triangle : si aire = 0, les points sont alignés
        Formule : aire = |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)| / 2
        """
        area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
        return area < 0.5  # Tolérance pour éviter les triangles trop plats
    
    def _generate_non_aligned_triangle_points(self, min_coord: int = 2, max_coord: int = 10) -> tuple:
        """
        Génère 3 points formant un vrai triangle (non alignés)
        Retourne : (x1, y1, x2, y2, x3, y3)
        """
        max_attempts = 50
        for _ in range(max_attempts):
            x1 = random.randint(min_coord, max_coord)
            y1 = random.randint(min_coord, max_coord)
            x2 = random.randint(min_coord, max_coord)
            y2 = random.randint(min_coord, max_coord)
            x3 = random.randint(min_coord, max_coord)
            y3 = random.randint(min_coord, max_coord)
            
            # Vérifier que les points ne sont pas alignés
            if not self._are_points_aligned(x1, y1, x2, y2, x3, y3):
                # Vérifier que les points sont suffisamment espacés
                dist_12 = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
                dist_23 = ((x3 - x2)**2 + (y3 - y2)**2)**0.5
                dist_31 = ((x1 - x3)**2 + (y1 - y3)**2)**0.5
                
                # Les côtés doivent avoir une longueur minimale de 2 unités
                if dist_12 >= 2 and dist_23 >= 2 and dist_31 >= 2:
                    return (x1, y1, x2, y2, x3, y3)
        
        # Fallback : triangle par défaut garantit non aligné
        return (3, 3, 7, 3, 5, 7)
    # === GÉNÉRATEURS SPÉCIALISÉS ===
    
    def _gen_triangle_rectangle(
        self, niveau: str, chapitre: str, difficulte: str
    ) -> MathExerciseSpec:
        """Génère un exercice de triangle rectangle (Pythagore)
        
        RÈGLE CRITIQUE : Toutes les longueurs dans l'énoncé (longueurs_connues) 
        doivent être des entiers ou décimaux simples, JAMAIS des valeurs irrationnelles.
        """
        
        points = self._get_next_geometry_points()
        angle_droit = points[1]  # Point de l'angle droit (milieu par défaut)
        
        # Triplets pythagoriciens exacts pour garantir des valeurs entières
        triplets_faciles = [
            (3, 4, 5), (5, 12, 13), (6, 8, 10), (7, 24, 25), 
            (8, 15, 17), (9, 12, 15), (9, 40, 41), (12, 16, 20)
        ]
        
        triplets_difficiles = [
            (11, 60, 61), (13, 84, 85), (20, 21, 29), (28, 45, 53),
            (33, 56, 65), (36, 77, 85), (5, 12, 13), (8, 15, 17)
        ]
        
        # Choisir un triplet selon la difficulté
        if difficulte == "facile":
            a, b, c = random.choice(triplets_faciles)
        else:
            a, b, c = random.choice(triplets_difficiles)
        
        # Décider quel côté calculer
        calcul_type = random.choice(["hypotenuse", "cote"])
        
        if calcul_type == "hypotenuse":
            # CAS 1 : Calculer l'hypoténuse
            # Donner les deux côtés de l'angle droit (a et b)
            # L'élève doit calculer l'hypoténuse (c)
            longueurs_connues = {
                f"{points[0]}{points[1]}": a,  # Premier côté
                f"{points[1]}{points[2]}": b   # Deuxième côté
            }
            longueur_a_calculer = f"{points[0]}{points[2]}"  # Hypoténuse
            resultat = c
            
            etapes = [
                f"Le triangle {points[0]}{points[1]}{points[2]} est rectangle en {angle_droit}",
                "D'après le théorème de Pythagore :",
                f"{longueur_a_calculer}² = {points[0]}{points[1]}² + {points[1]}{points[2]}²",
                f"{longueur_a_calculer}² = {a}² + {b}² = {a*a} + {b*b} = {a*a + b*b}",
                f"{longueur_a_calculer} = √{a*a + b*b} = {c} cm"
            ]
            
        else:
            # CAS 2 : Calculer un côté de l'angle droit
            # Donner l'hypoténuse (c) et un côté (a)
            # L'élève doit calculer l'autre côté (b)
            longueurs_connues = {
                f"{points[0]}{points[1]}": a,      # Côté connu
                f"{points[0]}{points[2]}": c       # Hypoténuse
            }
            longueur_a_calculer = f"{points[1]}{points[2]}"  # Côté à calculer
            resultat = b
            
            etapes = [
                f"Le triangle {points[0]}{points[1]}{points[2]} est rectangle en {angle_droit}",
                "D'après le théorème de Pythagore :",
                f"{points[0]}{points[2]}² = {points[0]}{points[1]}² + {longueur_a_calculer}²",
                f"{c}² = {a}² + {longueur_a_calculer}²",
                f"{longueur_a_calculer}² = {c}² - {a}² = {c*c} - {a*a} = {c*c - a*a}",
                f"{longueur_a_calculer} = √{c*c - a*a} = {b} cm"
            ]
        
        # Créer la figure géométrique avec UNIQUEMENT des valeurs entières
        figure = GeometricFigure(
            type="triangle_rectangle",
            points=points,
            rectangle_en=angle_droit,
            longueurs_connues=longueurs_connues,  # ✅ Uniquement des entiers
            longueurs_a_calculer=[longueur_a_calculer]
        )
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.TRIANGLE_RECTANGLE,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "type": "trouver_valeur",  # Type pédagogique pour gabarits
                "triangle": f"{points[0]}{points[1]}{points[2]}",
                "angle_droit": angle_droit,
                "longueurs_donnees": longueurs_connues,
                "longueur_a_calculer": longueur_a_calculer,
                "triplet_utilise": f"({a}, {b}, {c})"
            },
            solution_calculee={
                "longueur_calculee": resultat,
                "unite": "cm",
                "methode": "pythagore",
                "triplet": f"({a}, {b}, {c})"
            },
            etapes_calculees=etapes,
            resultat_final=f"{resultat} cm",  # ✅ Entier, pas de décimale
            figure_geometrique=figure,
            points_bareme=[
                {"etape": "Identification théorème de Pythagore", "points": 1.0},
                {"etape": "Application formule", "points": 2.0},
                {"etape": "Calcul et résultat", "points": 1.0}
            ]
        )
    
    def _gen_calcul_relatifs(
        self, niveau: str, chapitre: str, difficulte: str
    ) -> MathExerciseSpec:
        """Génère un exercice de calculs avec nombres relatifs"""
        
        if difficulte == "facile":
            operandes = [random.randint(-10, 10) for _ in range(3)]
            operations_list = ["+", "-"]
        else:
            operandes = [random.randint(-20, 20) for _ in range(4)]
            operations_list = ["+", "-", "*"] if difficulte == "difficile" else ["+", "-"]
        
        # Construire l'expression et stocker les opérations
        expression = str(operandes[0])
        operations_used = []
        
        for i in range(1, len(operandes)):
            op = random.choice(operations_list)
            operations_used.append(op)
            operand = operandes[i]
            
            if op == "+" and operand >= 0:
                expression += f" + {operand}"
            elif op == "+" and operand < 0:
                expression += f" + ({operand})"
            elif op == "-" and operand >= 0:
                expression += f" - {operand}"
            elif op == "-" and operand < 0:
                expression += f" - ({operand})"
            elif op == "*":
                expression += f" × {operand}"
        
        # Calculer le résultat correctement
        resultat = operandes[0]
        for i, op in enumerate(operations_used):
            operand = operandes[i + 1]
            if op == "+":
                resultat += operand
            elif op == "-":
                resultat -= operand
            elif op == "*":
                resultat *= operand
        
        # Construire les étapes
        etapes = [
            f"Expression à calculer : {expression}",
            "Calcul étape par étape :",
        ]
        
        # Détailler les étapes intermédiaires
        intermediate = operandes[0]
        for i, op in enumerate(operations_used):
            operand = operandes[i + 1]
            if op == "+":
                intermediate += operand
            elif op == "-":
                intermediate -= operand
            elif op == "*":
                intermediate *= operand
            etapes.append(f"= {intermediate}")
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.CALCUL_RELATIFS,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "expression": expression,
                "operandes": operandes,
                "operations": operations_used
            },
            solution_calculee={
                "resultat": resultat,
                "methode": "calcul_step_by_step"
            },
            etapes_calculees=etapes,
            resultat_final=resultat,
            points_bareme=[
                {"etape": "Organisation du calcul", "points": 1.0},
                {"etape": "Calculs intermédiaires", "points": 2.0},
                {"etape": "Résultat final", "points": 1.0}
            ]
        )
    
    def _gen_equation_1er_degre(
        self, niveau: str, chapitre: str, difficulte: str
    ) -> MathExerciseSpec:
        """Génère une équation du premier degré"""
        
        # Choisir la solution d'abord (pour éviter fractions complexes)
        x_solution = random.randint(1, 10) if difficulte == "facile" else random.randint(-5, 15)
        
        # Générer coefficients
        a = random.randint(2, 8)
        b = random.randint(-10, 10)
        
        # Calculer c pour que x_solution soit la solution
        c = a * x_solution + b
        
        equation = f"{a}x + {b} = {c}"
        
        etapes = [
            f"Équation : {equation}",
            f"{a}x = {c} - {b}",
            f"{a}x = {c - b}",
            f"x = {c - b} ÷ {a}",
            f"x = {x_solution}"
        ]
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.EQUATION_1ER_DEGRE,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "forme": "ax + b = c",
                "a": a,
                "b": b, 
                "c": c,
                "equation": equation
            },
            solution_calculee={
                "x": x_solution,
                "verification": f"{a} × {x_solution} + {b} = {a * x_solution + b}"
            },
            etapes_calculees=etapes,
            resultat_final=f"x = {x_solution}",
            points_bareme=[
                {"etape": "Isoler le terme en x", "points": 2.0},
                {"etape": "Division finale", "points": 1.0},
                {"etape": "Vérification", "points": 1.0}
            ]
        )
    
    # Générateurs supplémentaires (simplifiés pour l'exemple)
    
    def _gen_calcul_fractions(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice de calculs avec fractions (6e collège)"""
        
        if difficulte == "facile":
            # Fractions simples avec dénominateurs petits
            num1, den1 = random.randint(1, 5), random.choice([2, 3, 4, 5])
            num2, den2 = random.randint(1, 5), random.choice([2, 3, 4, 5])
        else:
            num1, den1 = random.randint(1, 10), random.randint(2, 12)
            num2, den2 = random.randint(1, 10), random.randint(2, 12)
        
        frac1 = Fraction(num1, den1)
        frac2 = Fraction(num2, den2)
        
        operation = random.choice(["+", "-"])
        
        if operation == "+":
            resultat = frac1 + frac2
            expression = f"\\frac{{{num1}}}{{{den1}}} + \\frac{{{num2}}}{{{den2}}}"
            op_texte = "la somme"
        else:
            resultat = frac1 - frac2
            expression = f"\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}}"
            op_texte = "la différence"
        
        # Calcul du dénominateur commun (PGCD)
        denom_commun = frac1.denominator * frac2.denominator // math.gcd(frac1.denominator, frac2.denominator)
        
        # Énoncé pédagogique complet
        enonce = f"Calculer {op_texte} des fractions suivantes et donner le résultat sous forme de fraction irréductible :\n\n{expression}"
        
        etapes = [
            f"Expression : {expression}",
            f"Dénominateur commun : {denom_commun}",
            f"Calcul : {expression} = \\frac{{{resultat.numerator}}}{{{resultat.denominator}}}"
        ]
        
        # Ajouter l'étape de simplification si applicable
        if resultat.numerator != num1 * den2 + num2 * den1 or resultat.denominator != denom_commun:
            etapes.append(f"Simplification : \\frac{{{resultat.numerator}}}{{{resultat.denominator}}}")
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.CALCUL_FRACTIONS,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "enonce": enonce,  # ✅ ÉNONCÉ DÉDIÉ pour éviter le fallback
                "fraction1": f"{num1}/{den1}",
                "fraction2": f"{num2}/{den2}",
                "operation": operation,
                "expression": expression
            },
            solution_calculee={
                "resultat_fraction": f"{resultat.numerator}/{resultat.denominator}",
                "resultat_decimal": float(resultat),
                "denom_commun": denom_commun
            },
            etapes_calculees=etapes,
            resultat_final=f"\\frac{{{resultat.numerator}}}{{{resultat.denominator}}}"
        )
    
    def _gen_calcul_decimaux(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice de calculs avec nombres décimaux"""
        
        if difficulte == "facile":
            a = round(random.uniform(1, 20), 1)
            b = round(random.uniform(1, 20), 1)
        else:
            a = round(random.uniform(5, 50), 2)
            b = round(random.uniform(5, 50), 2)
        
        operation = random.choice(["+", "-", "*"])
        
        if operation == "+":
            resultat = round(a + b, 2)
            expression = f"{a} + {b}"
            op_text = "addition"
        elif operation == "-":
            resultat = round(a - b, 2)
            expression = f"{a} - {b}"
            op_text = "soustraction"
        else:
            resultat = round(a * b, 2)
            expression = f"{a} × {b}"
            op_text = "multiplication"
        
        etapes = [
            f"Calcul : {expression}",
            f"Résultat : {resultat}"
        ]
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.CALCUL_DECIMAUX,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "a": a,
                "b": b,
                "operation": operation,
                "expression": expression
            },
            solution_calculee={
                "resultat": resultat,
                "operation": op_text
            },
            etapes_calculees=etapes,
            resultat_final=resultat
        )
    
    def _gen_triangle_quelconque(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice sur triangle quelconque (angles)"""
        
        points = self._get_next_geometry_points()
        
        # Générer deux angles, le troisième se déduit
        angle1 = random.randint(30, 80)
        angle2 = random.randint(30, 80)
        angle3 = 180 - angle1 - angle2
        
        # Vérifier que le troisième angle est valide
        if angle3 <= 0 or angle3 >= 150:
            angle1 = 60
            angle2 = 70
            angle3 = 50
        
        figure = GeometricFigure(
            type="triangle",
            points=points,
            angles_connus={
                f"{points[0]}{points[1]}{points[2]}": angle1,
                f"{points[1]}{points[2]}{points[0]}": angle2
            },
            angles_a_calculer=[f"{points[2]}{points[0]}{points[1]}"]
        )
        
        etapes = [
            f"Triangle {points[0]}{points[1]}{points[2]}",
            "La somme des angles d'un triangle est 180°",
            f"Angle en {points[0]} = {angle1}°, Angle en {points[1]} = {angle2}°",
            f"Angle en {points[2]} = 180° - {angle1}° - {angle2}° = {angle3}°"
        ]
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "triangle": f"{points[0]}{points[1]}{points[2]}",
                "angle1": angle1,
                "angle2": angle2
            },
            solution_calculee={
                "angle3": angle3
            },
            etapes_calculees=etapes,
            resultat_final=f"{angle3}°",
            figure_geometrique=figure
        )
    
    def _gen_proportionnalite(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice de proportionnalité"""
        
        # Coefficient de proportionnalité
        k = random.randint(2, 8)
        
        # Valeurs du tableau
        val1 = random.randint(3, 10)
        val2 = random.randint(12, 25)
        val3 = random.randint(5, 15)  # Valeur à trouver
        
        resultat1 = val1 * k
        resultat2 = val2 * k
        resultat_a_trouver = val3 * k
        
        # ✅ GÉNÉRER LE TABLEAU HTML pour l'énoncé
        tableau_html = f"""
<table style="border-collapse: collapse; margin: 15px auto; border: 2px solid #000; font-size: 14px;">
    <tr>
        <th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">Valeur</th>
        <th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">Résultat</th>
    </tr>
    <tr>
        <td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{val1}</td>
        <td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{resultat1}</td>
    </tr>
    <tr>
        <td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{val2}</td>
        <td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{resultat2}</td>
    </tr>
    <tr>
        <td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{val3}</td>
        <td style="border: 1px solid #000; padding: 8px 12px; text-align: center; background-color: #ffffcc; font-weight: bold;">?</td>
    </tr>
</table>
"""
        
        # Énoncé avec tableau HTML
        enonce = f"Compléter le tableau de proportionnalité suivant.{tableau_html}"
        
        etapes = [
            "Tableau de proportionnalité",
            f"{val1} → {resultat1}",
            f"{val2} → {resultat2}",
            f"Coefficient : {k}",
            f"{val3} → {val3} × {k} = {resultat_a_trouver}"
        ]
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.PROPORTIONNALITE,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "type": "trouver_valeur",  # Type pédagogique pour gabarits
                "enonce": enonce,  # ✅ ÉNONCÉ AVEC TABLEAU HTML
                "valeurs_donnees": [val1, val2],
                "resultats_donnes": [resultat1, resultat2],
                "valeur_a_trouver": val3,
                "coefficient": k,
                "tableau_html": tableau_html  # ✅ TABLEAU SÉPARÉ POUR RÉUTILISATION
            },
            solution_calculee={
                "resultat": resultat_a_trouver,
                "methode": "produit_en_croix"
            },
            etapes_calculees=etapes,
            resultat_final=resultat_a_trouver
        )
    
    def _gen_perimetre_aire(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice de périmètres et aires"""
        
        figure_type = random.choice(["rectangle", "carre", "cercle"])
        
        if figure_type == "rectangle":
            longueur = random.randint(8, 20)
            largeur = random.randint(4, 12)
            perimetre = 2 * (longueur + largeur)
            aire = longueur * largeur
            
            # Créer la figure géométrique du rectangle
            points = self._get_next_geometry_points()[:4]  # 4 points pour rectangle
            figure = GeometricFigure(
                type="rectangle",
                points=points,
                longueurs_connues={
                    f"{points[0]}{points[1]}": largeur,
                    f"{points[1]}{points[2]}": longueur
                },
                proprietes=["rectangle"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_valeur",  # Type pédagogique pour gabarits
                    "figure": "rectangle",
                    "longueur": longueur,
                    "largeur": largeur
                },
                solution_calculee={
                    "perimetre": perimetre,
                    "aire": aire
                },
                etapes_calculees=[
                    f"Rectangle de longueur {longueur} cm et largeur {largeur} cm",
                    f"Périmètre = 2 × ({longueur} + {largeur}) = {perimetre} cm",
                    f"Aire = {longueur} × {largeur} = {aire} cm²"
                ],
                resultat_final=f"Périmètre = {perimetre} cm, Aire = {aire} cm²",
                figure_geometrique=figure
            )
        
        elif figure_type == "carre":
            cote = random.randint(5, 15)
            perimetre = 4 * cote
            aire = cote * cote
            
            # Créer la figure géométrique du carré (rectangle avec longueur = largeur)
            points = self._get_next_geometry_points()[:4]
            figure = GeometricFigure(
                type="rectangle",
                points=points,
                longueurs_connues={
                    f"{points[0]}{points[1]}": cote,
                    f"{points[1]}{points[2]}": cote
                },
                proprietes=["carre", "rectangle"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_valeur",  # Type pédagogique pour gabarits
                    "figure": "carre",
                    "cote": cote
                },
                solution_calculee={
                    "perimetre": perimetre,
                    "aire": aire
                },
                etapes_calculees=[
                    f"Carré de côté {cote} cm",
                    f"Périmètre = 4 × {cote} = {perimetre} cm",
                    f"Aire = {cote}² = {aire} cm²"
                ],
                resultat_final=f"Périmètre = {perimetre} cm, Aire = {aire} cm²",
                figure_geometrique=figure
            )
        
        else:  # cercle
            rayon = random.randint(3, 10)
            perimetre = round(2 * math.pi * rayon, 2)
            aire = round(math.pi * rayon * rayon, 2)
            
            # Créer la figure géométrique du cercle
            figure = GeometricFigure(
                type="cercle",
                points=["O"],
                longueurs_connues={"rayon": rayon}
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_valeur",  # Type pédagogique pour gabarits
                    "figure": "cercle",
                    "rayon": rayon
                },
                solution_calculee={
                    "perimetre": perimetre,
                    "aire": aire
                },
                etapes_calculees=[
                    f"Cercle de rayon {rayon} cm",
                    f"Périmètre = 2 × π × {rayon} ≈ {perimetre} cm",
                    f"Aire = π × {rayon}² ≈ {aire} cm²"
                ],
                resultat_final=f"Périmètre ≈ {perimetre} cm, Aire ≈ {aire} cm²",
                figure_geometrique=figure
            )
    
    def _gen_rectangle(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Générateur pour rectangles"""
        # Obtenir 2 sets de points (3+3 = 6 points, on en utilisera 4)
        points_set1 = self._get_next_geometry_points()  # A, B, C
        points_set2 = self._get_next_geometry_points()  # D, E, F
        points = points_set1 + [points_set2[0]]  # A, B, C, D (4 points pour rectangle)
        
        # ✅ ASSERT : Garantir 4 points distincts pour rectangle
        assert len(points) == 4, f"Rectangle doit avoir 4 points, pas {len(points)}"
        assert len(set(points)) == 4, f"Rectangle doit avoir 4 points DISTINCTS: {points}"
        
        longueur = random.randint(8, 20)
        largeur = random.randint(4, 12)
        
        # ✅ ASSERT : Garantir valeurs positives
        assert longueur > 0 and largeur > 0, "Longueur et largeur doivent être > 0"
        
        figure = GeometricFigure(
            type="rectangle",
            points=points,
            longueurs_connues={
                f"{points[0]}{points[1]}": largeur,
                f"{points[1]}{points[2]}": longueur
            },
            proprietes=["rectangle"]
        )
        
        perimetre = 2 * (longueur + largeur)
        aire = longueur * largeur
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.RECTANGLE,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "longueur": longueur,
                "largeur": largeur,
                "rectangle": f"{points[0]}{points[1]}{points[2]}{points[3]}"
            },
            solution_calculee={
                "perimetre": perimetre,
                "aire": aire
            },
            etapes_calculees=[
                f"Rectangle {points[0]}{points[1]}{points[2]}{points[3]}",
                f"Longueur = {longueur} cm, largeur = {largeur} cm",
                f"Périmètre = 2 × ({longueur} + {largeur}) = {perimetre} cm",
                f"Aire = {longueur} × {largeur} = {aire} cm²"
            ],
            resultat_final=f"Périmètre = {perimetre} cm, Aire = {aire} cm²",
            figure_geometrique=figure
        )

    def _gen_volume(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice de calcul de volumes"""
        
        solides = ["cube", "pave", "cylindre", "prisme"]
        
        if difficulte == "facile":
            solides = ["cube", "pave"]
        
        solide = random.choice(solides)
        
        if solide == "cube":
            arete = random.randint(3, 12)
            volume = arete ** 3
            
            etapes = [
                f"Cube d'arête {arete} cm",
                "Volume = arête³",
                f"Volume = {arete}³ = {arete} × {arete} × {arete}",
                f"Volume = {volume} cm³"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.VOLUME,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "solide": "cube",
                    "arete": arete
                },
                solution_calculee={
                    "volume": volume,
                    "unite": "cm³"
                },
                etapes_calculees=etapes,
                resultat_final=f"{volume} cm³"
            )
        
        elif solide == "pave":
            longueur = random.randint(5, 15)
            largeur = random.randint(4, 12)
            hauteur = random.randint(3, 10)
            volume = longueur * largeur * hauteur
            
            etapes = [
                f"Pavé droit de dimensions {longueur} cm × {largeur} cm × {hauteur} cm",
                "Volume = longueur × largeur × hauteur",
                f"Volume = {longueur} × {largeur} × {hauteur}",
                f"Volume = {volume} cm³"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.VOLUME,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "solide": "pave",
                    "longueur": longueur,
                    "largeur": largeur,
                    "hauteur": hauteur
                },
                solution_calculee={
                    "volume": volume,
                    "unite": "cm³"
                },
                etapes_calculees=etapes,
                resultat_final=f"{volume} cm³"
            )
        
        elif solide == "cylindre":
            rayon = random.randint(3, 10)
            hauteur = random.randint(5, 15)
            volume = round(math.pi * rayon * rayon * hauteur, 2)
            
            etapes = [
                f"Cylindre de rayon {rayon} cm et hauteur {hauteur} cm",
                "Volume = π × rayon² × hauteur",
                f"Volume = π × {rayon}² × {hauteur}",
                f"Volume = π × {rayon * rayon} × {hauteur}",
                f"Volume ≈ {volume} cm³"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.VOLUME,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "solide": "cylindre",
                    "rayon": rayon,
                    "hauteur": hauteur
                },
                solution_calculee={
                    "volume": volume,
                    "unite": "cm³"
                },
                etapes_calculees=etapes,
                resultat_final=f"{volume} cm³"
            )
        
        else:  # prisme
            base_longueur = random.randint(5, 12)
            base_largeur = random.randint(4, 10)
            hauteur = random.randint(6, 15)
            aire_base = base_longueur * base_largeur
            volume = aire_base * hauteur
            
            etapes = [
                f"Prisme droit à base rectangulaire ({base_longueur} cm × {base_largeur} cm), hauteur {hauteur} cm",
                "Volume = aire de la base × hauteur",
                f"Aire de la base = {base_longueur} × {base_largeur} = {aire_base} cm²",
                f"Volume = {aire_base} × {hauteur} = {volume} cm³"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.VOLUME,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "solide": "prisme",
                    "base_longueur": base_longueur,
                    "base_largeur": base_largeur,
                    "hauteur": hauteur
                },
                solution_calculee={
                    "volume": volume,
                    "aire_base": aire_base,
                    "unite": "cm³"
                },
                etapes_calculees=etapes,
                resultat_final=f"{volume} cm³"
            )
    
    def _gen_statistiques(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice de statistiques (moyenne, médiane, étendue)"""
        
        # Générer une série de données
        if difficulte == "facile":
            nb_valeurs = random.randint(5, 8)
            valeurs = [random.randint(5, 20) for _ in range(nb_valeurs)]
        else:
            nb_valeurs = random.randint(8, 12)
            valeurs = [random.randint(0, 30) for _ in range(nb_valeurs)]
        
        # Calculs statistiques
        moyenne = round(sum(valeurs) / len(valeurs), 2)
        valeurs_triees = sorted(valeurs)
        
        # Médiane
        n = len(valeurs_triees)
        if n % 2 == 0:
            mediane = (valeurs_triees[n//2 - 1] + valeurs_triees[n//2]) / 2
        else:
            mediane = valeurs_triees[n//2]
        
        # Étendue
        etendue = max(valeurs) - min(valeurs)
        
        etapes = [
            f"Série de données : {valeurs}",
            f"Nombre de valeurs : {len(valeurs)}",
            f"Moyenne = somme / effectif = {sum(valeurs)} / {len(valeurs)} = {moyenne}",
            f"Série triée : {valeurs_triees}",
            f"Médiane = {mediane}",
            f"Étendue = max - min = {max(valeurs)} - {min(valeurs)} = {etendue}"
        ]
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.STATISTIQUES,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "valeurs": valeurs,
                "nb_valeurs": len(valeurs)
            },
            solution_calculee={
                "moyenne": moyenne,
                "mediane": mediane,
                "etendue": etendue,
                "min": min(valeurs),
                "max": max(valeurs)
            },
            etapes_calculees=etapes,
            resultat_final=f"Moyenne = {moyenne}, Médiane = {mediane}, Étendue = {etendue}"
        )
    
    def _gen_probabilites(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice de probabilités"""
        
        situations = [
            {
                "contexte": "dé",
                "nb_issues": 6,
                "question": "obtenir un nombre pair",
                "issues_favorables": 3
            },
            {
                "contexte": "dé",
                "nb_issues": 6,
                "question": "obtenir un nombre supérieur à 4",
                "issues_favorables": 2
            },
            {
                "contexte": "pièce",
                "nb_issues": 2,
                "question": "obtenir pile",
                "issues_favorables": 1
            },
            {
                "contexte": "sac avec 5 boules rouges et 3 boules bleues",
                "nb_issues": 8,
                "question": "tirer une boule rouge",
                "issues_favorables": 5
            }
        ]
        
        situation = random.choice(situations)
        
        probabilite = situation["issues_favorables"] / situation["nb_issues"]
        probabilite_fraction = Fraction(situation["issues_favorables"], situation["nb_issues"])
        
        etapes = [
            f"Expérience : {situation['contexte']}",
            f"Nombre d'issues possibles : {situation['nb_issues']}",
            f"Nombre d'issues favorables ({situation['question']}) : {situation['issues_favorables']}",
            "Probabilité = issues favorables / issues possibles",
            f"Probabilité = {situation['issues_favorables']} / {situation['nb_issues']}",
            f"Probabilité = {probabilite_fraction} = {probabilite:.2f}"
        ]
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.PROBABILITES,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "contexte": situation["contexte"],
                "question": situation["question"],
                "nb_issues": situation["nb_issues"],
                "issues_favorables": situation["issues_favorables"]
            },
            solution_calculee={
                "probabilite": probabilite,
                "fraction": f"{probabilite_fraction.numerator}/{probabilite_fraction.denominator}"
            },
            etapes_calculees=etapes,
            resultat_final=f"\\frac{{{probabilite_fraction.numerator}}}{{{probabilite_fraction.denominator}}}"
        )
    
    def _gen_puissances(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice sur les puissances"""
        
        type_calcul = random.choice(["calcul_simple", "produit", "quotient"])
        
        if type_calcul == "calcul_simple":
            base = random.randint(2, 10)
            exposant = random.randint(2, 5) if difficulte == "facile" else random.randint(3, 6)
            resultat = base ** exposant
            
            etapes = [
                f"Calculer {base}^{{{exposant}}}",
                f"{base}^{{{exposant}}} = " + " × ".join([str(base)] * exposant),
                f"{base}^{{{exposant}}} = {resultat}"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PUISSANCES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calcul_simple",
                    "base": base,
                    "exposant": exposant
                },
                solution_calculee={
                    "resultat": resultat
                },
                etapes_calculees=etapes,
                resultat_final=resultat
            )
        
        elif type_calcul == "produit":
            base = random.randint(2, 8)
            exp1 = random.randint(2, 4)
            exp2 = random.randint(2, 4)
            exp_somme = exp1 + exp2
            resultat = base ** exp_somme
            
            etapes = [
                f"Calculer {base}^{{{exp1}}} × {base}^{{{exp2}}}",
                "Propriété : a^m × a^n = a^(m+n)",
                f"{base}^{{{exp1}}} × {base}^{{{exp2}}} = {base}^{{{exp1}+{exp2}}}",
                f"{base}^{{{exp1}}} × {base}^{{{exp2}}} = {base}^{{{exp_somme}}}",
                f"{base}^{{{exp_somme}}} = {resultat}"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PUISSANCES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "produit",
                    "base": base,
                    "exposant1": exp1,
                    "exposant2": exp2
                },
                solution_calculee={
                    "exposant_somme": exp_somme,
                    "resultat": resultat
                },
                etapes_calculees=etapes,
                resultat_final=resultat
            )
        
        else:  # quotient
            base = random.randint(2, 8)
            exp1 = random.randint(4, 7)
            exp2 = random.randint(2, exp1-1)  # exp2 < exp1 pour éviter exposants négatifs
            exp_diff = exp1 - exp2
            resultat = base ** exp_diff
            
            etapes = [
                f"Calculer {base}^{{{exp1}}} ÷ {base}^{{{exp2}}}",
                "Propriété : a^m ÷ a^n = a^(m-n)",
                f"{base}^{{{exp1}}} ÷ {base}^{{{exp2}}} = {base}^{{{exp1}-{exp2}}}",
                f"{base}^{{{exp1}}} ÷ {base}^{{{exp2}}} = {base}^{{{exp_diff}}}",
                f"{base}^{{{exp_diff}}} = {resultat}"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PUISSANCES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "quotient",
                    "base": base,
                    "exposant1": exp1,
                    "exposant2": exp2
                },
                solution_calculee={
                    "exposant_diff": exp_diff,
                    "resultat": resultat
                },
                etapes_calculees=etapes,
                resultat_final=resultat
            )

    def _gen_cercle(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice sur les cercles (périmètre, aire)"""
        
        type_calcul = random.choice(["perimetre", "aire", "rayon_depuis_perimetre"])
        
        if type_calcul == "perimetre":
            rayon = random.randint(3, 15)
            perimetre = round(2 * math.pi * rayon, 2)
            
            etapes = [
                f"Cercle de rayon {rayon} cm",
                "Périmètre = 2 × π × rayon",
                f"Périmètre = 2 × π × {rayon}",
                f"Périmètre ≈ {perimetre} cm"
            ]
            
            # Créer la figure géométrique
            figure = GeometricFigure(
                type="cercle",
                points=["O"],
                longueurs_connues={"rayon": rayon}
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CERCLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "perimetre",
                    "rayon": rayon
                },
                solution_calculee={
                    "perimetre": perimetre,
                    "unite": "cm"
                },
                etapes_calculees=etapes,
                resultat_final=f"{perimetre} cm",
                figure_geometrique=figure
            )
        
        elif type_calcul == "aire":
            rayon = random.randint(3, 12)
            aire = round(math.pi * rayon * rayon, 2)
            
            etapes = [
                f"Cercle de rayon {rayon} cm",
                "Aire = π × rayon²",
                f"Aire = π × {rayon}²",
                f"Aire = π × {rayon * rayon}",
                f"Aire ≈ {aire} cm²"
            ]
            
            # Créer la figure géométrique
            figure = GeometricFigure(
                type="cercle",
                points=["O"],
                longueurs_connues={"rayon": rayon}
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CERCLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "aire",
                    "rayon": rayon
                },
                solution_calculee={
                    "aire": aire,
                    "unite": "cm²"
                },
                etapes_calculees=etapes,
                resultat_final=f"{aire} cm²",
                figure_geometrique=figure
            )
        
        else:  # rayon depuis périmètre
            rayon = random.randint(5, 12)
            perimetre = round(2 * math.pi * rayon, 2)
            
            etapes = [
                f"Périmètre du cercle = {perimetre} cm",
                "Périmètre = 2 × π × rayon",
                f"{perimetre} = 2 × π × rayon",
                f"rayon = {perimetre} / (2 × π)",
                f"rayon ≈ {rayon} cm"
            ]
            
            # Créer la figure géométrique
            figure = GeometricFigure(
                type="cercle",
                points=["O"],
                longueurs_connues={"rayon": rayon}
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CERCLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "rayon_depuis_perimetre",
                    "perimetre": perimetre
                },
                solution_calculee={
                    "rayon": rayon,
                    "unite": "cm"
                },
                etapes_calculees=etapes,
                resultat_final=f"{rayon} cm",
                figure_geometrique=figure
            )
    
    def _gen_thales(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice sur le théorème de Thalès"""
        
        # Obtenir 2 sets de points (3+3 = 6 points, on en utilisera 5)
        points_set1 = self._get_next_geometry_points()  # A, B, C
        points_set2 = self._get_next_geometry_points()  # D, E, F (on prendra D, E)
        points = points_set1 + points_set2[:2]  # A, B, C, D, E
        
        # Configuration : triangle ABC avec droite (DE) parallèle à (BC)
        # D sur [AB], E sur [AC]
        
        # Choisir des rapports simples
        if difficulte == "facile":
            rapports = [2, 3, 4]
            k = random.choice(rapports)
        else:
            k = random.randint(2, 5)
        
        # Longueurs
        AD = random.randint(3, 8)
        AE = random.randint(3, 8)
        
        # DB = k × AD (pour que AB = AD + DB)
        DB = k * AD
        AB = AD + DB
        
        # EC = k × AE
        EC = k * AE
        AC = AE + EC
        
        # DE = BC / k (proportionnalité)
        BC = random.randint(10, 20)
        DE = round(BC / (k + 1), 2)
        
        # Configuration : points[0]=A (sommet), points[1]=B, points[2]=C (base)
        # points[3]=D (sur AB), points[4]=E (sur AC)
        # Parallèle : (DE) // (BC)
        A, B, C, D, E = points[0], points[1], points[2], points[3], points[4]
        
        etapes = [
            f"Triangle {A}{B}{C} avec ({D}{E}) // ({B}{C})",
            f"{D} sur [{A}{B}], {E} sur [{A}{C}]",
            "D'après le théorème de Thalès :",
            f"{A}{D}/{A}{B} = {A}{E}/{A}{C} = {D}{E}/{B}{C}",
            f"{AD}/{AB} = {AE}/{AC}",
            f"Rapport = {AD}/{AB} = {AD}/{AD + DB} ≈ {round(AD/AB, 2)}"
        ]
        
        figure = GeometricFigure(
            type="thales",
            points=points[:5],
            longueurs_connues={
                f"{points[0]}{points[3]}": AD,
                f"{points[3]}{points[1]}": DB,
                f"{points[0]}{points[4]}": AE,
                f"{points[4]}{points[2]}": EC
            },
            proprietes=["thales", f"({points[3]}{points[4]}) // ({points[1]}{points[2]})"]
        )
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.THALES,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "points": points[:5],
                "AD": AD,
                "DB": DB,
                "AE": AE,
                "EC": EC,
                "rapport": round(AD/AB, 2)
            },
            solution_calculee={
                "AB": AB,
                "AC": AC,
                "rapport": round(AD/AB, 2)
            },
            etapes_calculees=etapes,
            resultat_final=f"Rapport = {round(AD/AB, 2)}",
            figure_geometrique=figure
        )
    
    def _gen_trigonometrie(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Génère un exercice de trigonométrie"""
        
        points = self._get_next_geometry_points()
        
        # Angles remarquables
        angles_remarquables = {
            30: {"sin": 0.5, "cos": round(math.sqrt(3)/2, 4), "tan": round(1/math.sqrt(3), 4)},
            45: {"sin": round(math.sqrt(2)/2, 4), "cos": round(math.sqrt(2)/2, 4), "tan": 1.0},
            60: {"sin": round(math.sqrt(3)/2, 4), "cos": 0.5, "tan": round(math.sqrt(3), 4)}
        }
        
        if difficulte == "facile":
            angle = random.choice([30, 45, 60])
        else:
            angle = random.randint(25, 70)
        
        type_calcul = random.choice(["cote_oppose", "cote_adjacent", "hypotenuse"])
        
        if type_calcul == "cote_oppose":
            # Calculer le côté opposé avec sin
            hypotenuse = random.randint(10, 20)
            
            if angle in angles_remarquables:
                sin_angle = angles_remarquables[angle]["sin"]
            else:
                sin_angle = round(math.sin(math.radians(angle)), 4)
            
            cote_oppose = round(hypotenuse * sin_angle, 2)
            
            etapes = [
                f"Triangle rectangle {points[0]}{points[1]}{points[2]}",
                f"Angle en {points[0]} = {angle}°",
                f"Hypoténuse {points[0]}{points[2]} = {hypotenuse} cm",
                f"sin({angle}°) = côté opposé / hypoténuse",
                f"sin({angle}°) = {points[1]}{points[2]} / {hypotenuse}",
                f"{points[1]}{points[2]} = {hypotenuse} × sin({angle}°)",
                f"{points[1]}{points[2]} ≈ {cote_oppose} cm"
            ]
            
            resultat = cote_oppose
            
        elif type_calcul == "cote_adjacent":
            # Calculer le côté adjacent avec cos
            hypotenuse = random.randint(10, 20)
            
            if angle in angles_remarquables:
                cos_angle = angles_remarquables[angle]["cos"]
            else:
                cos_angle = round(math.cos(math.radians(angle)), 4)
            
            cote_adjacent = round(hypotenuse * cos_angle, 2)
            
            etapes = [
                f"Triangle rectangle {points[0]}{points[1]}{points[2]}",
                f"Angle en {points[0]} = {angle}°",
                f"Hypoténuse = {hypotenuse} cm",
                f"cos({angle}°) = côté adjacent / hypoténuse",
                f"côté adjacent = {hypotenuse} × cos({angle}°)",
                f"côté adjacent ≈ {cote_adjacent} cm"
            ]
            
            resultat = cote_adjacent
            
        else:  # hypotenuse
            cote_oppose = random.randint(5, 12)
            
            if angle in angles_remarquables:
                sin_angle = angles_remarquables[angle]["sin"]
            else:
                sin_angle = round(math.sin(math.radians(angle)), 4)
            
            hypotenuse = round(cote_oppose / sin_angle, 2)
            
            etapes = [
                f"Triangle rectangle, angle = {angle}°",
                f"Côté opposé = {cote_oppose} cm",
                f"sin({angle}°) = {cote_oppose} / hypoténuse",
                f"hypoténuse = {cote_oppose} / sin({angle}°)",
                f"hypoténuse ≈ {hypotenuse} cm"
            ]
            
            resultat = hypotenuse
        
        figure = GeometricFigure(
            type="triangle_rectangle",
            points=points[:3],
            rectangle_en=points[1],
            angles_connus={points[0]: angle}
        )
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.TRIGONOMETRIE,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "triangle": f"{points[0]}{points[1]}{points[2]}",
                "angle": angle,
                "type_calcul": type_calcul
            },
            solution_calculee={
                "resultat": resultat,
                "unite": "cm",
                "angle": angle
            },
            etapes_calculees=etapes,
            resultat_final=f"{resultat} cm",
            figure_geometrique=figure
        )
    
    def _gen_symetrie_axiale(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice de symétrie axiale
        Concepts :
        - Trouver le symétrique d'un point par rapport à un axe
        - Vérifier si deux points sont symétriques
        - Propriétés : distances égales à l'axe, perpendiculaire à l'axe
        """
        
        points = self._get_next_geometry_points()
        
        # Types d'exercices possibles
        types_exercices = ["trouver_symetrique", "verifier_symetrie", "completer_figure"]
        
        if difficulte == "facile":
            type_exercice = "trouver_symetrique"
            # Axe simple (vertical ou horizontal)
            axe_type = random.choice(["vertical", "horizontal"])
        else:
            type_exercice = random.choice(types_exercices)
            # Peut inclure des axes obliques
            axe_type = random.choice(["vertical", "horizontal", "oblique"])
        
        if type_exercice == "trouver_symetrique":
            # Point original
            point_original = points[0]
            point_image = points[1]
            
            if axe_type == "vertical":
                # Axe vertical (ex: x = 3)
                axe_position = random.randint(3, 8)
                # Point original à gauche ou droite de l'axe
                point_x = random.randint(0, axe_position - 1) if random.random() < 0.5 else random.randint(axe_position + 1, 12)
                point_y = random.randint(2, 10)
                
                # Calcul du symétrique
                distance_axe = abs(point_x - axe_position)
                if point_x < axe_position:
                    image_x = axe_position + distance_axe
                else:
                    image_x = axe_position - distance_axe
                image_y = point_y
                
                axe_description = f"l'axe vertical passant par x = {axe_position}"
                etapes = [
                    f"Point {point_original}({point_x}, {point_y})",
                    f"Axe de symétrie : droite verticale x = {axe_position}",
                    f"Distance de {point_original} à l'axe : |{point_x} - {axe_position}| = {distance_axe}",
                    f"Le symétrique {point_image} est à la même distance de l'autre côté de l'axe",
                    f"Coordonnées de {point_image} : ({image_x}, {image_y})"
                ]
                
            elif axe_type == "horizontal":
                # Axe horizontal (ex: y = 5)
                axe_position = random.randint(4, 8)
                point_x = random.randint(2, 10)
                # Point original au-dessus ou en-dessous de l'axe
                point_y = random.randint(0, axe_position - 1) if random.random() < 0.5 else random.randint(axe_position + 1, 12)
                
                # Calcul du symétrique
                distance_axe = abs(point_y - axe_position)
                image_x = point_x
                if point_y < axe_position:
                    image_y = axe_position + distance_axe
                else:
                    image_y = axe_position - distance_axe
                
                axe_description = f"l'axe horizontal passant par y = {axe_position}"
                etapes = [
                    f"Point {point_original}({point_x}, {point_y})",
                    f"Axe de symétrie : droite horizontale y = {axe_position}",
                    f"Distance de {point_original} à l'axe : |{point_y} - {axe_position}| = {distance_axe}",
                    f"Le symétrique {point_image} est à la même distance de l'autre côté de l'axe",
                    f"Coordonnées de {point_image} : ({image_x}, {image_y})"
                ]
                
            else:  # oblique (niveau difficile)
                # Axe oblique simplifié : première diagonale (y = x)
                point_x = random.randint(2, 10)
                point_y = random.randint(2, 10)
                # Symétrique par rapport à y = x : on échange x et y
                image_x = point_y
                image_y = point_x
                
                axe_description = "la première bissectrice (y = x)"
                etapes = [
                    f"Point {point_original}({point_x}, {point_y})",
                    f"Axe de symétrie : première bissectrice (y = x)",
                    f"Propriété : le symétrique d'un point par rapport à y = x s'obtient en échangeant x et y",
                    f"Coordonnées de {point_image} : ({image_x}, {image_y})"
                ]
            
            # Créer la figure géométrique
            figure = GeometricFigure(
                type="symetrie_axiale",
                points=[point_original, point_image],
                longueurs_connues={
                    f"{point_original}_x": point_x,
                    f"{point_original}_y": point_y,
                    f"{point_image}_x": image_x,
                    f"{point_image}_y": image_y
                },
                proprietes=[f"axe_{axe_type}", f"axe_position_{axe_position if axe_type != 'oblique' else 'y=x'}"]
            )
            
            # ✅ ÉNONCÉ PÉDAGOGIQUE DÉDIÉ pour éviter le fallback
            enonce = f"Construire le symétrique du point {point_original}({point_x} ; {point_y}) par rapport à {axe_description}."
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_AXIALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "enonce": enonce,  # ✅ ÉNONCÉ DÉDIÉ
                    "type": "trouver_symetrique",
                    "point_original": point_original,
                    "point_image": point_image,
                    "axe_type": axe_type,
                    "axe_description": axe_description,
                    "point_original_coords": {"x": point_x, "y": point_y}
                },
                solution_calculee={
                    "image_coords": {"x": image_x, "y": image_y},
                    "distance_axe": distance_axe if axe_type != "oblique" else "N/A"
                },
                etapes_calculees=etapes,
                resultat_final=f"{point_image}({image_x}, {image_y})",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Identification de l'axe", "points": 1.0},
                    {"etape": "Calcul de la distance à l'axe", "points": 1.5},
                    {"etape": "Construction du symétrique", "points": 1.5}
                ],
                conseils_prof=[
                    "Vérifier que l'élève trace bien la perpendiculaire à l'axe",
                    "Vérifier que les distances de part et d'autre de l'axe sont égales"
                ]
            )
        
        elif type_exercice == "verifier_symetrie":
            # Vérifier si deux points sont symétriques par rapport à un axe
            point_a = points[0]
            point_b = points[1]
            
            # Créer deux cas : symétriques ou non
            sont_symetriques = random.choice([True, False])
            
            if axe_type == "vertical":
                axe_position = random.randint(4, 8)
                point_a_x = random.randint(1, axe_position - 1)
                point_a_y = random.randint(3, 10)
                
                if sont_symetriques:
                    distance = axe_position - point_a_x
                    point_b_x = axe_position + distance
                    point_b_y = point_a_y
                else:
                    # Créer un point non symétrique
                    point_b_x = random.randint(axe_position + 1, 12)
                    point_b_y = point_a_y + random.randint(1, 3)  # Différent en y
                
                axe_description = f"l'axe vertical x = {axe_position}"
                
                distance_a = abs(point_a_x - axe_position)
                distance_b = abs(point_b_x - axe_position)
                
                etapes = [
                    f"Points : {point_a}({point_a_x}, {point_a_y}) et {point_b}({point_b_x}, {point_b_y})",
                    f"Axe : droite verticale x = {axe_position}",
                    f"Distance de {point_a} à l'axe : {distance_a}",
                    f"Distance de {point_b} à l'axe : {distance_b}",
                    f"Ordonnées : {point_a_y} et {point_b_y}"
                ]
                
                if sont_symetriques:
                    etapes.append(f"Les distances sont égales ({distance_a} = {distance_b}) et les ordonnées identiques")
                    etapes.append(f"Conclusion : {point_a} et {point_b} sont symétriques par rapport à l'axe")
                else:
                    if distance_a != distance_b:
                        etapes.append(f"Les distances sont différentes ({distance_a} ≠ {distance_b})")
                    if point_a_y != point_b_y:
                        etapes.append(f"Les ordonnées sont différentes ({point_a_y} ≠ {point_b_y})")
                    etapes.append(f"Conclusion : {point_a} et {point_b} ne sont PAS symétriques par rapport à l'axe")
            
            elif axe_type == "horizontal":
                axe_position = random.randint(4, 8)
                point_a_x = random.randint(3, 10)
                point_a_y = random.randint(1, axe_position - 1)
                
                if sont_symetriques:
                    distance = axe_position - point_a_y
                    point_b_x = point_a_x
                    point_b_y = axe_position + distance
                else:
                    point_b_x = point_a_x + random.randint(1, 3)
                    point_b_y = random.randint(axe_position + 1, 12)
                
                axe_description = f"l'axe horizontal y = {axe_position}"
                
                distance_a = abs(point_a_y - axe_position)
                distance_b = abs(point_b_y - axe_position)
                
                etapes = [
                    f"Points : {point_a}({point_a_x}, {point_a_y}) et {point_b}({point_b_x}, {point_b_y})",
                    f"Axe : droite horizontale y = {axe_position}",
                    f"Distance de {point_a} à l'axe : {distance_a}",
                    f"Distance de {point_b} à l'axe : {distance_b}",
                    f"Abscisses : {point_a_x} et {point_b_x}"
                ]
                
                if sont_symetriques:
                    etapes.append(f"Les distances sont égales ({distance_a} = {distance_b}) et les abscisses identiques")
                    etapes.append(f"Conclusion : {point_a} et {point_b} sont symétriques par rapport à l'axe")
                else:
                    if distance_a != distance_b:
                        etapes.append(f"Les distances sont différentes ({distance_a} ≠ {distance_b})")
                    if point_a_x != point_b_x:
                        etapes.append(f"Les abscisses sont différentes ({point_a_x} ≠ {point_b_x})")
                    etapes.append(f"Conclusion : {point_a} et {point_b} ne sont PAS symétriques par rapport à l'axe")
            
            else:  # oblique (y = x)
                # Pour l'axe y = x, les coordonnées sont échangées
                point_a_x = random.randint(2, 7)
                point_a_y = random.randint(2, 10)
                
                if sont_symetriques:
                    # Symétrique par rapport à y = x : échanger x et y
                    point_b_x = point_a_y
                    point_b_y = point_a_x
                else:
                    # Créer un point non symétrique
                    point_b_x = random.randint(2, 10)
                    point_b_y = random.randint(2, 10)
                    # S'assurer qu'il n'est pas symétrique par hasard
                    while point_b_x == point_a_y and point_b_y == point_a_x:
                        point_b_x = random.randint(2, 10)
                        point_b_y = random.randint(2, 10)
                
                axe_description = "la droite y = x"
                axe_position = "y=x"
                
                etapes = [
                    f"Points : {point_a}({point_a_x}, {point_a_y}) et {point_b}({point_b_x}, {point_b_y})",
                    f"Axe : droite oblique y = x",
                    f"Pour la symétrie par rapport à y = x, les coordonnées doivent être échangées",
                    f"Si {point_a} est symétrique de {point_b}, alors {point_b} devrait avoir les coordonnées ({point_a_y}, {point_a_x})"
                ]
                
                if sont_symetriques:
                    etapes.append(f"Vérification : {point_b}({point_b_x}, {point_b_y}) = ({point_a_y}, {point_a_x}) ✓")
                    etapes.append(f"Conclusion : {point_a} et {point_b} sont symétriques par rapport à y = x")
                else:
                    etapes.append(f"Vérification : {point_b}({point_b_x}, {point_b_y}) ≠ ({point_a_y}, {point_a_x})")
                    etapes.append(f"Conclusion : {point_a} et {point_b} ne sont PAS symétriques par rapport à y = x")
                
                distance_a = 0  # Pas pertinent pour y = x
                distance_b = 0
            
            figure = GeometricFigure(
                type="symetrie_axiale",
                points=[point_a, point_b],
                longueurs_connues={
                    f"{point_a}_x": point_a_x,
                    f"{point_a}_y": point_a_y,
                    f"{point_b}_x": point_b_x,
                    f"{point_b}_y": point_b_y
                },
                proprietes=[f"axe_{axe_type}", f"axe_position_{axe_position}", f"symetriques_{sont_symetriques}"]
            )
            
            # ✅ ÉNONCÉ PÉDAGOGIQUE DÉDIÉ
            enonce = f"Les points {point_a}({point_a_x} ; {point_a_y}) et {point_b}({point_b_x} ; {point_b_y}) sont-ils symétriques par rapport à {axe_description} ? Justifier."
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_AXIALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "enonce": enonce,  # ✅ ÉNONCÉ DÉDIÉ
                    "type": "verifier_symetrie",
                    "point_a": point_a,
                    "point_b": point_b,
                    "axe_type": axe_type,
                    "axe_description": axe_description,
                    "coords_a": {"x": point_a_x, "y": point_a_y},
                    "coords_b": {"x": point_b_x, "y": point_b_y}
                },
                solution_calculee={
                    "sont_symetriques": sont_symetriques,
                    "distance_a": distance_a,
                    "distance_b": distance_b
                },
                etapes_calculees=etapes,
                resultat_final="Oui, ils sont symétriques" if sont_symetriques else "Non, ils ne sont pas symétriques",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Calcul des distances à l'axe", "points": 2.0},
                    {"etape": "Vérification coordonnée constante", "points": 1.0},
                    {"etape": "Conclusion", "points": 1.0}
                ]
            )
        
        else:  # completer_figure
            # Compléter une figure par symétrie
            # Triangle dont on donne la moitié
            point_a = points[0]
            point_b = points[1]
            point_c = points[2]
            
            axe_type = "vertical"
            axe_position = 6
            
            # Générer un vrai triangle non aligné à gauche de l'axe
            x1, y1, x2, y2, x3, y3 = self._generate_non_aligned_triangle_points(min_coord=2, max_coord=axe_position-1)
            
            coords = {
                point_a: {"x": x1, "y": y1},
                point_b: {"x": x2, "y": y2},
                point_c: {"x": x3, "y": y3}
            }
            
            # Symétriques
            point_a_prime = f"{point_a}'"
            point_b_prime = f"{point_b}'"
            point_c_prime = f"{point_c}'"
            
            coords_symetriques = {
                point_a_prime: {"x": 2 * axe_position - coords[point_a]["x"], "y": coords[point_a]["y"]},
                point_b_prime: {"x": 2 * axe_position - coords[point_b]["x"], "y": coords[point_b]["y"]},
                point_c_prime: {"x": 2 * axe_position - coords[point_c]["x"], "y": coords[point_c]["y"]}
            }
            
            etapes = [
                f"Triangle {point_a}{point_b}{point_c} avec {point_a}({coords[point_a]['x']}, {coords[point_a]['y']}), "
                f"{point_b}({coords[point_b]['x']}, {coords[point_b]['y']}), {point_c}({coords[point_c]['x']}, {coords[point_c]['y']})",
                f"Axe de symétrie : droite verticale x = {axe_position}",
                f"Pour chaque point, calculer son symétrique :",
                f"{point_a}' ({coords_symetriques[point_a_prime]['x']}, {coords_symetriques[point_a_prime]['y']})",
                f"{point_b}' ({coords_symetriques[point_b_prime]['x']}, {coords_symetriques[point_b_prime]['y']})",
                f"{point_c}' ({coords_symetriques[point_c_prime]['x']}, {coords_symetriques[point_c_prime]['y']})"
            ]
            
            all_points = [point_a, point_b, point_c]
            
            # Convertir coords en format plat pour GeometricFigure
            longueurs_converties = {}
            for pt, coord in coords.items():
                longueurs_converties[f"{pt}_x"] = coord["x"]
                longueurs_converties[f"{pt}_y"] = coord["y"]
            for pt, coord in coords_symetriques.items():
                longueurs_converties[f"{pt}_x"] = coord["x"]
                longueurs_converties[f"{pt}_y"] = coord["y"]
            
            figure = GeometricFigure(
                type="symetrie_axiale",
                points=all_points,
                longueurs_connues=longueurs_converties,
                proprietes=[f"axe_vertical", f"axe_position_{axe_position}", "triangle", "with_grid"]
            )
            
            # ✅ ÉNONCÉ PÉDAGOGIQUE DÉDIÉ
            enonce = f"Construire le symétrique du triangle {point_a}{point_b}{point_c} par rapport à l'axe vertical passant par x = {axe_position}."
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_AXIALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "enonce": enonce,  # ✅ ÉNONCÉ DÉDIÉ
                    "type": "completer_figure",
                    "figure": "triangle",
                    "points_initiaux": all_points,
                    "axe_position": axe_position
                },
                solution_calculee={
                    "points_symetriques": coords_symetriques
                },
                etapes_calculees=etapes,
                resultat_final=f"Triangle symétrique : {point_a}'{point_b}'{point_c}'",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Construction des symétriques", "points": 3.0},
                    {"etape": "Tracé de la figure complète", "points": 1.0}
                ]
            )
    
    def _gen_symetrie_centrale(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice de symétrie centrale (5e)
        
        Concepts :
        - Trouver le symétrique d'un point par rapport à un centre
        - Le centre est le milieu du segment [MM']
        - Formule : M' = 2*O - M où O est le centre de symétrie
        """
        
        points = self._get_next_geometry_points()
        
        # Types d'exercices possibles
        types_exercices = ["trouver_symetrique", "verifier_symetrie", "completer_figure"]
        
        if difficulte == "facile":
            type_exercice = "trouver_symetrique"
        else:
            type_exercice = random.choice(types_exercices)
        
        if type_exercice == "trouver_symetrique":
            # Trouver le symétrique d'un point par rapport à un centre
            point_original = points[0]
            centre = points[1]
            point_image = points[2]
            
            # Coordonnées du centre
            centre_x = random.randint(4, 8)
            centre_y = random.randint(4, 8)
            
            # Coordonnées du point original
            # Choisir un point pas trop loin du centre
            point_x = random.randint(max(1, centre_x - 4), min(12, centre_x + 4))
            point_y = random.randint(max(1, centre_y - 4), min(12, centre_y + 4))
            
            # Éviter que le point soit sur le centre
            if point_x == centre_x and point_y == centre_y:
                point_x += 2
            
            # Calcul du symétrique par symétrie centrale
            # Formule : M' = 2*O - M
            image_x = 2 * centre_x - point_x
            image_y = 2 * centre_y - point_y
            
            # Vérifier que l'image est dans les limites
            if image_x < 0 or image_x > 14 or image_y < 0 or image_y > 14:
                # Recalculer avec un point plus proche du centre
                point_x = centre_x + random.choice([-2, -1, 1, 2])
                point_y = centre_y + random.choice([-2, -1, 1, 2])
                image_x = 2 * centre_x - point_x
                image_y = 2 * centre_y - point_y
            
            # Calcul des distances (pour vérification pédagogique)
            distance_M_O = ((point_x - centre_x)**2 + (point_y - centre_y)**2)**0.5
            distance_O_M_prime = ((image_x - centre_x)**2 + (image_y - centre_y)**2)**0.5
            
            etapes = [
                f"Point {point_original}({point_x}, {point_y})",
                f"Centre de symétrie {centre}({centre_x}, {centre_y})",
                f"Formule : {point_image} = 2 × {centre} - {point_original}",
                f"Coordonnée x de {point_image} : 2 × {centre_x} - {point_x} = {image_x}",
                f"Coordonnée y de {point_image} : 2 × {centre_y} - {point_y} = {image_y}",
                f"Vérification : {centre} est le milieu de [{point_original}{point_image}]",
                f"Distance {point_original}{centre} = {distance_M_O:.2f}",
                f"Distance {centre}{point_image} = {distance_O_M_prime:.2f}",
                f"Coordonnées de {point_image} : ({image_x}, {image_y})"
            ]
            
            # Créer la figure géométrique
            figure = GeometricFigure(
                type="symetrie_centrale",
                points=[point_original, centre, point_image],
                longueurs_connues={
                    f"{point_original}_x": point_x,
                    f"{point_original}_y": point_y,
                    f"{centre}_x": centre_x,
                    f"{centre}_y": centre_y,
                    f"{point_image}_x": image_x,
                    f"{point_image}_y": image_y
                },
                proprietes=["centre_symetrie"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_CENTRALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_symetrique",
                    "point_original": point_original,
                    "centre": centre,
                    "point_image": point_image,
                    "point_original_coords": {"x": point_x, "y": point_y},
                    "centre_coords": {"x": centre_x, "y": centre_y}
                },
                solution_calculee={
                    "image_coords": {"x": image_x, "y": image_y},
                    "distance_M_O": round(distance_M_O, 2),
                    "distance_O_M_prime": round(distance_O_M_prime, 2)
                },
                etapes_calculees=etapes,
                resultat_final=f"{point_image}({image_x}, {image_y})",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Identification du centre", "points": 1.0},
                    {"etape": "Application de la formule", "points": 2.0},
                    {"etape": "Coordonnées correctes", "points": 1.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève utilise bien la formule M' = 2O - M",
                    "S'assurer que l'élève vérifie que O est le milieu"
                ]
            )
        
        elif type_exercice == "verifier_symetrie":
            # Vérifier si deux points sont symétriques par rapport à un centre
            point_a = points[0]
            centre = points[1]
            point_b = points[2]
            
            # Créer deux cas : symétriques ou non
            sont_symetriques = random.choice([True, False])
            
            # Centre
            centre_x = random.randint(5, 9)
            centre_y = random.randint(5, 9)
            
            # Point A
            point_a_x = random.randint(2, centre_x - 1)
            point_a_y = random.randint(2, centre_y - 1)
            
            if sont_symetriques:
                # Calculer le vrai symétrique
                point_b_x = 2 * centre_x - point_a_x
                point_b_y = 2 * centre_y - point_a_y
            else:
                # Créer un point non symétrique (décalé)
                point_b_x = 2 * centre_x - point_a_x + random.randint(1, 2)
                point_b_y = 2 * centre_y - point_a_y + random.randint(1, 2)
            
            # Calcul du milieu de [AB]
            milieu_x = (point_a_x + point_b_x) / 2
            milieu_y = (point_a_y + point_b_y) / 2
            
            # Distances
            distance_A_O = ((point_a_x - centre_x)**2 + (point_a_y - centre_y)**2)**0.5
            distance_O_B = ((point_b_x - centre_x)**2 + (point_b_y - centre_y)**2)**0.5
            
            etapes = [
                f"Points : {point_a}({point_a_x}, {point_a_y}) et {point_b}({point_b_x}, {point_b_y})",
                f"Centre proposé : {centre}({centre_x}, {centre_y})",
                f"Pour que {point_a} et {point_b} soient symétriques par rapport à {centre} :",
                f"  → {centre} doit être le milieu de [{point_a}{point_b}]",
                f"Milieu de [{point_a}{point_b}] : ({milieu_x}, {milieu_y})",
                f"Coordonnées de {centre} : ({centre_x}, {centre_y})"
            ]
            
            if sont_symetriques:
                etapes.append(f"Le milieu correspond à {centre} ✓")
                etapes.append(f"Distance {point_a}{centre} = {distance_A_O:.2f}")
                etapes.append(f"Distance {centre}{point_b} = {distance_O_B:.2f}")
                etapes.append(f"Les distances sont égales ✓")
                etapes.append(f"Conclusion : {point_a} et {point_b} sont symétriques par rapport à {centre}")
            else:
                if milieu_x != centre_x or milieu_y != centre_y:
                    etapes.append(f"Le milieu ({milieu_x}, {milieu_y}) ≠ {centre}({centre_x}, {centre_y}) ✗")
                etapes.append(f"Conclusion : {point_a} et {point_b} ne sont PAS symétriques par rapport à {centre}")
            
            figure = GeometricFigure(
                type="symetrie_centrale",
                points=[point_a, centre, point_b],
                longueurs_connues={
                    f"{point_a}_x": point_a_x,
                    f"{point_a}_y": point_a_y,
                    f"{centre}_x": centre_x,
                    f"{centre}_y": centre_y,
                    f"{point_b}_x": point_b_x,
                    f"{point_b}_y": point_b_y
                },
                proprietes=[f"centre_symetrie", f"symetriques_{sont_symetriques}"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_CENTRALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "verifier_symetrie",
                    "point_a": point_a,
                    "centre": centre,
                    "point_b": point_b,
                    "coords_a": {"x": point_a_x, "y": point_a_y},
                    "coords_centre": {"x": centre_x, "y": centre_y},
                    "coords_b": {"x": point_b_x, "y": point_b_y}
                },
                solution_calculee={
                    "sont_symetriques": sont_symetriques,
                    "milieu": {"x": milieu_x, "y": milieu_y},
                    "distance_A_O": round(distance_A_O, 2),
                    "distance_O_B": round(distance_O_B, 2)
                },
                etapes_calculees=etapes,
                resultat_final="Oui, ils sont symétriques" if sont_symetriques else "Non, ils ne sont pas symétriques",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Calcul du milieu", "points": 2.0},
                    {"etape": "Vérification distances", "points": 1.0},
                    {"etape": "Conclusion", "points": 1.0}
                ]
            )
        
        else:  # completer_figure
            # Compléter une figure par symétrie centrale - TRIANGLE
            point_a = points[0]
            point_b = points[1]
            point_c = points[3] if len(points) > 3 else "P"  # 3ème sommet du triangle
            centre = points[2]
            
            # Centre
            centre_x = 7
            centre_y = 6
            
            # Générer un vrai triangle non aligné
            x1, y1, x2, y2, x3, y3 = self._generate_non_aligned_triangle_points(min_coord=3, max_coord=10)
            
            coords_originaux = {
                point_a: {"x": x1, "y": y1},
                point_b: {"x": x2, "y": y2},
                point_c: {"x": x3, "y": y3}
            }
            
            # Symétriques des 3 sommets
            point_a_prime = f"{point_a}'"
            point_b_prime = f"{point_b}'"
            point_c_prime = f"{point_c}'"
            
            coords_symetriques = {
                point_a_prime: {
                    "x": 2 * centre_x - coords_originaux[point_a]["x"],
                    "y": 2 * centre_y - coords_originaux[point_a]["y"]
                },
                point_b_prime: {
                    "x": 2 * centre_x - coords_originaux[point_b]["x"],
                    "y": 2 * centre_y - coords_originaux[point_b]["y"]
                },
                point_c_prime: {
                    "x": 2 * centre_x - coords_originaux[point_c]["x"],
                    "y": 2 * centre_y - coords_originaux[point_c]["y"]
                }
            }
            
            etapes = [
                f"Triangle {point_a}{point_b}{point_c} avec {point_a}({coords_originaux[point_a]['x']}, {coords_originaux[point_a]['y']}), "
                f"{point_b}({coords_originaux[point_b]['x']}, {coords_originaux[point_b]['y']}), "
                f"{point_c}({coords_originaux[point_c]['x']}, {coords_originaux[point_c]['y']})",
                f"Centre de symétrie {centre}({centre_x}, {centre_y})",
                f"Pour chaque point, calculer son symétrique avec la formule M' = 2O - M :",
                f"{point_a_prime} : (2×{centre_x} - {coords_originaux[point_a]['x']}, "
                f"2×{centre_y} - {coords_originaux[point_a]['y']}) = "
                f"({coords_symetriques[point_a_prime]['x']}, {coords_symetriques[point_a_prime]['y']})",
                f"{point_b_prime} : (2×{centre_x} - {coords_originaux[point_b]['x']}, "
                f"2×{centre_y} - {coords_originaux[point_b]['y']}) = "
                f"({coords_symetriques[point_b_prime]['x']}, {coords_symetriques[point_b_prime]['y']})",
                f"{point_c_prime} : (2×{centre_x} - {coords_originaux[point_c]['x']}, "
                f"2×{centre_y} - {coords_originaux[point_c]['y']}) = "
                f"({coords_symetriques[point_c_prime]['x']}, {coords_symetriques[point_c_prime]['y']})"
            ]
            
            # Convertir coords en format plat
            longueurs_converties = {}
            for pt, coord in coords_originaux.items():
                longueurs_converties[f"{pt}_x"] = coord["x"]
                longueurs_converties[f"{pt}_y"] = coord["y"]
            for pt, coord in coords_symetriques.items():
                longueurs_converties[f"{pt}_x"] = coord["x"]
                longueurs_converties[f"{pt}_y"] = coord["y"]
            longueurs_converties[f"{centre}_x"] = centre_x
            longueurs_converties[f"{centre}_y"] = centre_y
            
            all_points = [point_a, point_b, point_c, centre]
            
            figure = GeometricFigure(
                type="symetrie_centrale",
                points=all_points,
                longueurs_connues=longueurs_converties,
                proprietes=["centre_symetrie", "figure_complete", "triangle", "with_grid"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_CENTRALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "completer_figure",
                    "figure": "triangle",
                    "points_initiaux": all_points,
                    "centre": centre
                },
                solution_calculee={
                    "points_symetriques": coords_symetriques
                },
                etapes_calculees=etapes,
                resultat_final=f"Triangle symétrique : {point_a_prime}{point_b_prime}{point_c_prime}",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Construction des symétriques", "points": 3.0},
                    {"etape": "Tracé de la figure complète", "points": 1.0}
                ]
            )    # ========== SPRINT 1 : Générateurs 6e (G03, N03, SP01) ==========
    
    def _gen_perpendiculaires_paralleles(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur les perpendiculaires et parallèles (6e_G03)
        
        Concepts :
        - Tracer une perpendiculaire à une droite passant par un point
        - Tracer une parallèle à une droite passant par un point
        - Identifier des droites perpendiculaires/parallèles
        """
        
        points = self._get_next_geometry_points()
        
        types_exercices = ["tracer_perpendiculaire", "tracer_parallele", "identifier"]
        
        if difficulte == "facile":
            type_exercice = "tracer_perpendiculaire"
        else:
            type_exercice = random.choice(types_exercices)
        
        if type_exercice == "tracer_perpendiculaire":
            # Tracer une perpendiculaire à une droite passant par un point
            droite = f"({points[0]}{points[1]})"
            point = points[2]
            
            # Coordonnées pour le schéma
            if difficulte == "facile":
                point_A_x = random.randint(2, 6)
                point_A_y = random.randint(4, 8)
                point_B_x = random.randint(10, 14)
                point_B_y = random.randint(4, 8)
                point_C_x = random.randint(6, 10)
                point_C_y = random.randint(10, 14)
            else:
                point_A_x = random.randint(1, 5)
                point_A_y = random.randint(2, 10)
                point_B_x = random.randint(11, 15)
                point_B_y = random.randint(2, 10)
                point_C_x = random.randint(4, 12)
                point_C_y = random.randint(8, 15)
            
            etapes = [
                f"Tracer la perpendiculaire à la droite {droite} passant par le point {point}",
                f"Méthode :",
                f"1. Placer l'équerre le long de la droite {droite}",
                f"2. Faire glisser l'équerre jusqu'au point {point}",
                f"3. Tracer la droite perpendiculaire",
                f"Vérification : l'angle formé doit être de 90°"
            ]
            
            figure = GeometricFigure(
                type="perpendiculaires_paralleles",
                points=[points[0], points[1], points[2]],
                longueurs_connues={
                    f"{points[0]}_x": point_A_x,
                    f"{points[0]}_y": point_A_y,
                    f"{points[1]}_x": point_B_x,
                    f"{points[1]}_y": point_B_y,
                    f"{points[2]}_x": point_C_x,
                    f"{points[2]}_y": point_C_y
                },
                proprietes=["perpendiculaire", "with_grid"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.RECTANGLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "tracer_perpendiculaire",
                    "droite": droite,
                    "point": point,
                    "enonce": f"Tracer la perpendiculaire à la droite {droite} passant par le point {point}. Utiliser l'équerre."
                },
                solution_calculee={
                    "angle": 90,
                    "methode": "équerre"
                },
                etapes_calculees=etapes,
                resultat_final="Droite perpendiculaire tracée",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Positionnement équerre", "points": 1.0},
                    {"etape": "Tracé perpendiculaire", "points": 1.0}
                ],
                conseils_prof=[
                    "Vérifier que l'équerre est bien positionnée le long de la droite",
                    "Vérifier que la perpendiculaire passe bien par le point donné"
                ]
            )
        
        elif type_exercice == "tracer_parallele":
            # Tracer une parallèle à une droite passant par un point
            droite = f"({points[0]}{points[1]})"
            point = points[2]
            
            # Coordonnées
            if difficulte == "facile":
                point_A_x = random.randint(2, 6)
                point_A_y = random.randint(3, 6)
                point_B_x = random.randint(10, 14)
                point_B_y = random.randint(3, 6)
                point_C_x = random.randint(2, 6)
                point_C_y = random.randint(10, 14)
            else:
                point_A_x = random.randint(1, 5)
                point_A_y = random.randint(2, 8)
                point_B_x = random.randint(11, 15)
                point_B_y = random.randint(2, 8)
                point_C_x = random.randint(1, 5)
                point_C_y = random.randint(9, 15)
            
            etapes = [
                f"Tracer la parallèle à la droite {droite} passant par le point {point}",
                f"Méthode :",
                f"1. Placer la règle le long de la droite {droite}",
                f"2. Placer l'équerre contre la règle",
                f"3. Faire glisser l'ensemble jusqu'au point {point}",
                f"4. Tracer la droite parallèle",
                f"Vérification : les deux droites ne se coupent jamais"
            ]
            
            figure = GeometricFigure(
                type="perpendiculaires_paralleles",
                points=[points[0], points[1], points[2]],
                longueurs_connues={
                    f"{points[0]}_x": point_A_x,
                    f"{points[0]}_y": point_A_y,
                    f"{points[1]}_x": point_B_x,
                    f"{points[1]}_y": point_B_y,
                    f"{points[2]}_x": point_C_x,
                    f"{points[2]}_y": point_C_y
                },
                proprietes=["parallele", "with_grid"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.RECTANGLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "tracer_parallele",
                    "droite": droite,
                    "point": point,
                    "enonce": f"Tracer la parallèle à la droite {droite} passant par le point {point}. Utiliser la règle et l'équerre."
                },
                solution_calculee={
                    "methode": "règle_et_équerre"
                },
                etapes_calculees=etapes,
                resultat_final="Droite parallèle tracée",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Positionnement règle et équerre", "points": 1.0},
                    {"etape": "Tracé parallèle", "points": 1.0}
                ],
                conseils_prof=[
                    "Vérifier que la règle et l'équerre sont bien positionnées",
                    "Vérifier que la parallèle passe bien par le point donné"
                ]
            )
        
        else:  # identifier
            # Identifier des droites perpendiculaires ou parallèles
            # ✅ FIX: Obtenir un set supplémentaire car on a besoin de 4 points (2 droites)
            points_set2 = self._get_next_geometry_points()
            all_points = points + [points_set2[0]]  # Ajouter le 4ème point
            
            droite1 = f"({all_points[0]}{all_points[1]})"
            droite2 = f"({all_points[2]}{all_points[3]})"
            
            relation = random.choice(["perpendiculaires", "parallèles", "quelconques"])
            
            etapes = [
                f"Observer les droites {droite1} et {droite2}",
                f"Méthode :",
                f"1. Placer l'équerre sur les deux droites",
                f"2. Vérifier si elles forment un angle de 90° (perpendiculaires)",
                f"3. Ou vérifier si elles ne se coupent jamais (parallèles)",
                f"Résultat : les droites sont {relation}"
            ]
            
            # Coordonnées selon la relation
            if relation == "perpendiculaires":
                point_A_x, point_A_y = random.randint(2, 6), random.randint(4, 8)
                point_B_x, point_B_y = random.randint(10, 14), random.randint(4, 8)
                point_C_x, point_C_y = random.randint(6, 10), random.randint(10, 14)
                point_D_x, point_D_y = random.randint(6, 10), random.randint(2, 4)
                proprietes = ["perpendiculaire", "with_grid"]
            elif relation == "parallèles":
                point_A_x, point_A_y = random.randint(2, 6), random.randint(3, 6)
                point_B_x, point_B_y = random.randint(10, 14), random.randint(3, 6)
                point_C_x, point_C_y = random.randint(2, 6), random.randint(10, 14)
                point_D_x, point_D_y = random.randint(10, 14), random.randint(10, 14)
                proprietes = ["parallele", "with_grid"]
            else:
                point_A_x, point_A_y = random.randint(2, 6), random.randint(3, 6)
                point_B_x, point_B_y = random.randint(10, 14), random.randint(5, 9)
                point_C_x, point_C_y = random.randint(1, 5), random.randint(10, 14)
                point_D_x, point_D_y = random.randint(11, 15), random.randint(12, 15)
                proprietes = ["with_grid"]
            
            figure = GeometricFigure(
                type="perpendiculaires_paralleles",
                points=[all_points[0], all_points[1], all_points[2], all_points[3]],
                longueurs_connues={
                    f"{all_points[0]}_x": point_A_x,
                    f"{all_points[0]}_y": point_A_y,
                    f"{all_points[1]}_x": point_B_x,
                    f"{all_points[1]}_y": point_B_y,
                    f"{all_points[2]}_x": point_C_x,
                    f"{all_points[2]}_y": point_C_y,
                    f"{all_points[3]}_x": point_D_x,
                    f"{all_points[3]}_y": point_D_y
                },
                proprietes=proprietes
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.RECTANGLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "identifier",
                    "droite1": droite1,
                    "droite2": droite2,
                    "enonce": f"Observer les droites {droite1} et {droite2}. Dire si elles sont perpendiculaires, parallèles ou quelconques."
                },
                solution_calculee={
                    "relation": relation
                },
                etapes_calculees=etapes,
                resultat_final=f"Les droites sont {relation}",
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Observation", "points": 1.0},
                    {"etape": "Identification", "points": 1.0}
                ]
            )
    
    def _gen_droite_numerique(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur la droite numérique et le repérage (6e_N03)
        
        Concepts :
        - Placer un nombre sur la droite graduée
        - Lire l'abscisse d'un point
        - Calculer la distance entre deux points
        """
        
        types_exercices = ["placer_nombre", "lire_abscisse", "calculer_distance"]
        
        if difficulte == "facile":
            type_exercice = "lire_abscisse"
        else:
            type_exercice = random.choice(types_exercices)
        
        # Définir l'échelle de la droite selon la difficulté
        if difficulte == "facile":
            min_val = 0
            max_val = 10
            graduation = 1
        elif difficulte == "moyen":
            min_val = 0
            max_val = 50
            graduation = 5
        else:  # difficile
            min_val = -20
            max_val = 20
            graduation = 2
        
        if type_exercice == "placer_nombre":
            # Placer un nombre sur la droite
            nombre = min_val + random.randint(1, (max_val - min_val) // graduation) * graduation
            
            etapes = [
                f"Placer le nombre {nombre} sur la droite graduée",
                f"Méthode :",
                f"1. Observer l'échelle : les graduations vont de {min_val} à {max_val} par pas de {graduation}",
                f"2. Compter les graduations depuis {min_val}",
                f"3. Marquer le point à la position {nombre}"
            ]
            
            enonce = f"Sur une droite graduée allant de {min_val} à {max_val} (graduations tous les {graduation}), placer le point A d'abscisse {nombre}."
            
            # ✅ CRÉER LA FIGURE GÉOMÉTRIQUE (droite graduée)
            figure = GeometricFigure(
                type="droite_numerique",
                points=["A"],
                longueurs_connues={
                    "min": min_val,
                    "max": max_val,
                    "graduation": graduation,
                    "point_A_abscisse": nombre  # Point à placer (pour correction)
                },
                proprietes=["placer_nombre", "with_graduations"]
            )
            
        elif type_exercice == "lire_abscisse":
            # Lire l'abscisse d'un point
            position = random.randint(1, (max_val - min_val) // graduation)
            abscisse = min_val + position * graduation
            
            etapes = [
                f"Lire l'abscisse du point A",
                f"Méthode :",
                f"1. Repérer l'origine ({min_val}) sur la droite",
                f"2. Compter les graduations jusqu'au point A",
                f"3. Multiplier par la graduation ({graduation})",
                f"Résultat : abscisse = {abscisse}"
            ]
            
            enonce = f"Sur une droite graduée allant de {min_val} à {max_val} (graduations tous les {graduation}), le point A est placé. Lire son abscisse."
            
            # ✅ CRÉER LA FIGURE GÉOMÉTRIQUE (droite graduée avec point)
            figure = GeometricFigure(
                type="droite_numerique",
                points=["A"],
                longueurs_connues={
                    "min": min_val,
                    "max": max_val,
                    "graduation": graduation,
                    "point_A_abscisse": abscisse  # Point déjà placé
                },
                proprietes=["lire_abscisse", "with_graduations", "show_point_A"]
            )
            
        else:  # calculer_distance
            # Calculer la distance entre deux points
            pos1 = random.randint(1, (max_val - min_val) // (graduation * 2))
            pos2 = random.randint(pos1 + 2, (max_val - min_val) // graduation)
            
            abscisse1 = min_val + pos1 * graduation
            abscisse2 = min_val + pos2 * graduation
            distance = abs(abscisse2 - abscisse1)
            
            etapes = [
                f"Calculer la distance entre A et B",
                f"Point A : abscisse = {abscisse1}",
                f"Point B : abscisse = {abscisse2}",
                f"Méthode :",
                f"Distance = |abscisse de B - abscisse de A|",
                f"Distance = |{abscisse2} - {abscisse1}|",
                f"Distance = {distance}"
            ]
            
            enonce = f"Sur une droite graduée, le point A a pour abscisse {abscisse1} et le point B a pour abscisse {abscisse2}. Calculer la distance AB."
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer_distance",
                    "abscisse1": abscisse1,
                    "abscisse2": abscisse2,
                    "enonce": enonce
                },
                solution_calculee={
                    "distance": distance,
                    "methode": "valeur_absolue"
                },
                etapes_calculees=etapes,
                resultat_final=str(distance),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Identification des abscisses", "points": 1.0},
                    {"etape": "Calcul de la distance", "points": 1.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève utilise la valeur absolue",
                    "Insister sur le fait que la distance est toujours positive"
                ]
            )
        
        # Pour les types "placer_nombre" et "lire_abscisse"
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.CALCUL_DECIMAUX,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "type": type_exercice,
                "min_val": min_val,
                "max_val": max_val,
                "graduation": graduation,
                "nombre": nombre if type_exercice == "placer_nombre" else abscisse,
                "enonce": enonce
            },
            solution_calculee={
                "abscisse": nombre if type_exercice == "placer_nombre" else abscisse,
                "methode": "graduation"
            },
            etapes_calculees=etapes,
            resultat_final=str(nombre if type_exercice == "placer_nombre" else abscisse),
            figure_geometrique=figure,  # ✅ AJOUT DE LA FIGURE
            points_bareme=[
                {"etape": "Lecture/placement correct", "points": 2.0}
            ],
            conseils_prof=[
                "Vérifier que l'élève respecte l'échelle de graduation",
                "Insister sur la précision du placement"
            ]
        )
    
    def _gen_tableaux_donnees(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur les tableaux de données (6e_SP01)
        
        Concepts :
        - Lire un tableau de données
        - Compléter un tableau
        - Calculer des totaux
        """
        
        types_exercices = ["lire_tableau", "completer_tableau", "calculer_total"]
        
        if difficulte == "facile":
            type_exercice = "lire_tableau"
            nb_lignes = 2
            nb_colonnes = 3
        elif difficulte == "moyen":
            type_exercice = random.choice(["lire_tableau", "completer_tableau"])
            nb_lignes = 3
            nb_colonnes = 4
        else:  # difficile
            type_exercice = random.choice(types_exercices)
            nb_lignes = 4
            nb_colonnes = 5
        
        # Thèmes possibles
        themes = [
            {"nom": "notes", "lignes": ["Mathématiques", "Français", "Histoire"], "colonnes": ["Trimestre 1", "Trimestre 2", "Trimestre 3"]},
            {"nom": "ventes", "lignes": ["Lundi", "Mardi", "Mercredi"], "colonnes": ["Pommes", "Bananes", "Oranges"]},
            {"nom": "temperatures", "lignes": ["Lundi", "Mardi", "Mercredi"], "colonnes": ["Matin", "Midi", "Soir"]}
        ]
        
        theme = random.choice(themes)
        
        # Générer les données selon la difficulté
        if difficulte == "facile":
            donnees = [[random.randint(10, 20) for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        elif difficulte == "moyen":
            donnees = [[random.randint(5, 50) for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        else:
            donnees = [[random.randint(1, 100) for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        
        if type_exercice == "lire_tableau":
            # Lire une valeur dans le tableau
            ligne = random.randint(0, nb_lignes - 1)
            colonne = random.randint(0, nb_colonnes - 1)
            valeur = donnees[ligne][colonne]
            
            nom_ligne = theme["lignes"][ligne % len(theme["lignes"])]
            nom_colonne = theme["colonnes"][colonne % len(theme["colonnes"])]
            
            # ✅ GÉNÉRER LE TABLEAU HTML
            tableau_html = '<table style="border-collapse: collapse; margin: 15px auto; border: 2px solid #000; font-size: 14px;">'
            
            # En-tête du tableau
            tableau_html += '<tr><th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0;"></th>'
            for col_name in theme["colonnes"][:nb_colonnes]:
                tableau_html += f'<th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">{col_name}</th>'
            tableau_html += '</tr>'
            
            # Lignes de données
            for i, row in enumerate(donnees[:nb_lignes]):
                row_name = theme["lignes"][i % len(theme["lignes"])]
                tableau_html += f'<tr><th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">{row_name}</th>'
                for j, cell_value in enumerate(row[:nb_colonnes]):
                    # Mettre en évidence la cellule à lire
                    if i == ligne and j == colonne:
                        tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center; background-color: #ffffcc; font-weight: bold;">?</td>'
                    else:
                        tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{cell_value}</td>'
                tableau_html += '</tr>'
            
            tableau_html += '</table>'
            
            etapes = [
                f"Lire la valeur dans le tableau",
                f"Ligne : {nom_ligne}",
                f"Colonne : {nom_colonne}",
                f"Valeur : {valeur}"
            ]
            
            enonce = f"Dans le tableau de {theme['nom']} ci-dessous, quelle est la valeur pour {nom_ligne} dans la colonne {nom_colonne} ?{tableau_html}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.STATISTIQUES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "lire_tableau",
                    "donnees": donnees,
                    "ligne": ligne,
                    "colonne": colonne,
                    "nom_ligne": nom_ligne,
                    "nom_colonne": nom_colonne,
                    "enonce": enonce,
                    "tableau_html": tableau_html  # ✅ TABLEAU HTML AJOUTÉ
                },
                solution_calculee={
                    "valeur": valeur
                },
                etapes_calculees=etapes,
                resultat_final=str(valeur),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Lecture correcte", "points": 2.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève repère bien la ligne et la colonne",
                    "Insister sur la lecture méthodique"
                ]
            )
        
        elif type_exercice == "completer_tableau":
            # Compléter une valeur manquante
            ligne = random.randint(0, nb_lignes - 1)
            colonne = random.randint(0, nb_colonnes - 1)
            valeur_manquante = donnees[ligne][colonne]
            
            # Recalculer le total avant de cacher la valeur
            total_ligne = sum(donnees[ligne])
            
            # Cacher la valeur
            donnees[ligne][colonne] = None
            total_sans_manquante = sum(v for v in donnees[ligne] if v is not None)
            
            nom_ligne = theme["lignes"][ligne % len(theme["lignes"])]
            
            # ✅ GÉNÉRER LE TABLEAU HTML
            tableau_html = '<table style="border-collapse: collapse; margin: 15px auto; border: 2px solid #000; font-size: 14px;">'
            
            # En-tête du tableau
            tableau_html += '<tr><th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0;"></th>'
            for col_name in theme["colonnes"][:nb_colonnes]:
                tableau_html += f'<th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">{col_name}</th>'
            tableau_html += '<th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">Total</th></tr>'
            
            # Lignes de données
            for i, row in enumerate(donnees[:nb_lignes]):
                row_name = theme["lignes"][i % len(theme["lignes"])]
                tableau_html += f'<tr><th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">{row_name}</th>'
                for j, cell_value in enumerate(row[:nb_colonnes]):
                    # Mettre en évidence la cellule manquante
                    if i == ligne and j == colonne:
                        tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center; background-color: #ffffcc; font-weight: bold;">?</td>'
                    elif cell_value is None:
                        tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">-</td>'
                    else:
                        tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{cell_value}</td>'
                
                # Colonne Total
                if i == ligne:
                    tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center; font-weight: bold;">{total_ligne}</td>'
                else:
                    row_total = sum(v for v in row if v is not None)
                    tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{row_total}</td>'
                
                tableau_html += '</tr>'
            
            tableau_html += '</table>'
            
            etapes = [
                f"Compléter le tableau",
                f"Ligne : {nom_ligne}",
                f"Total de la ligne : {total_ligne}",
                f"Somme des valeurs connues : {total_sans_manquante}",
                f"Valeur manquante = {total_ligne} - {total_sans_manquante} = {valeur_manquante}"
            ]
            
            enonce = f"Dans le tableau de {theme['nom']} ci-dessous, la ligne {nom_ligne} a un total de {total_ligne}. Quelle est la valeur manquante ?{tableau_html}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.STATISTIQUES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "completer_tableau",
                    "total_ligne": total_ligne,
                    "total_sans_manquante": total_sans_manquante,
                    "nom_ligne": nom_ligne,
                    "enonce": enonce,
                    "tableau_html": tableau_html  # ✅ TABLEAU HTML AJOUTÉ
                },
                solution_calculee={
                    "valeur_manquante": valeur_manquante
                },
                etapes_calculees=etapes,
                resultat_final=str(valeur_manquante),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Compréhension du problème", "points": 1.0},
                    {"etape": "Calcul de la valeur manquante", "points": 1.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève comprend le principe du total",
                    "Insister sur la soustraction pour trouver la valeur manquante"
                ]
            )
        
        else:  # calculer_total
            # Calculer le total d'une ligne ou colonne
            choix = random.choice(["ligne", "colonne"])
            
            # ✅ GÉNÉRER LE TABLEAU HTML COMPLET
            tableau_html = '<table style="border-collapse: collapse; margin: 15px auto; border: 2px solid #000; font-size: 14px;">'
            
            # En-tête du tableau
            tableau_html += '<tr><th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0;"></th>'
            for col_name in theme["colonnes"][:nb_colonnes]:
                tableau_html += f'<th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">{col_name}</th>'
            tableau_html += '</tr>'
            
            if choix == "ligne":
                ligne = random.randint(0, nb_lignes - 1)
                total = sum(donnees[ligne])
                nom = theme["lignes"][ligne % len(theme["lignes"])]
                
                # Lignes de données avec mise en évidence
                for i, row in enumerate(donnees[:nb_lignes]):
                    row_name = theme["lignes"][i % len(theme["lignes"])]
                    if i == ligne:
                        # Ligne à calculer - mise en évidence
                        tableau_html += f'<tr style="background-color: #fff3cd;"><th style="border: 1px solid #000; padding: 8px 12px; background-color: #ffc107; font-weight: bold;">{row_name}</th>'
                    else:
                        tableau_html += f'<tr><th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">{row_name}</th>'
                    
                    for cell_value in row[:nb_colonnes]:
                        tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{cell_value}</td>'
                    tableau_html += '</tr>'
                
                tableau_html += '</table>'
                
                etapes = [
                    f"Calculer le total de la ligne {nom}",
                    f"Valeurs : {' + '.join(map(str, donnees[ligne]))}",
                    f"Total = {total}"
                ]
                
                enonce = f"Dans le tableau de {theme['nom']} ci-dessous, calculer le total de la ligne {nom}.{tableau_html}"
            else:
                colonne = random.randint(0, nb_colonnes - 1)
                total = sum(donnees[i][colonne] for i in range(nb_lignes))
                nom = theme["colonnes"][colonne % len(theme["colonnes"])]
                
                valeurs_colonne = [donnees[i][colonne] for i in range(nb_lignes)]
                
                # Lignes de données avec mise en évidence de la colonne
                for i, row in enumerate(donnees[:nb_lignes]):
                    row_name = theme["lignes"][i % len(theme["lignes"])]
                    tableau_html += f'<tr><th style="border: 1px solid #000; padding: 8px 12px; background-color: #f0f0f0; font-weight: bold;">{row_name}</th>'
                    
                    for j, cell_value in enumerate(row[:nb_colonnes]):
                        if j == colonne:
                            # Colonne à calculer - mise en évidence
                            tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center; background-color: #fff3cd; font-weight: bold;">{cell_value}</td>'
                        else:
                            tableau_html += f'<td style="border: 1px solid #000; padding: 8px 12px; text-align: center;">{cell_value}</td>'
                    tableau_html += '</tr>'
                
                tableau_html += '</table>'
                
                etapes = [
                    f"Calculer le total de la colonne {nom}",
                    f"Valeurs : {' + '.join(map(str, valeurs_colonne))}",
                    f"Total = {total}"
                ]
                
                enonce = f"Dans le tableau de {theme['nom']} ci-dessous, calculer le total de la colonne {nom}.{tableau_html}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.STATISTIQUES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer_total",
                    "choix": choix,
                    "nom": nom,
                    "enonce": enonce,
                    "tableau_html": tableau_html  # ✅ TABLEAU HTML AJOUTÉ
                },
                solution_calculee={
                    "total": total
                },
                etapes_calculees=etapes,
                resultat_final=str(total),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Addition des valeurs", "points": 2.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève additionne toutes les valeurs",
                    "Insister sur la vérification du calcul"
                ]
            )

    
    # ============================================================================
    # SPRINT 2 - GÉNÉRATEURS 6e (G01, G02, N01, N02, N04)
    # ============================================================================
    
    def _gen_points_segments_droites(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur points, segments, droites, demi-droites (6e_G01)
        
        Concepts :
        - Identifier segment, droite, demi-droite
        - Nommer correctement une figure
        - Tracer une figure selon consignes
        """
        
        points = self._get_next_geometry_points()
        
        types_exercices = ["identifier", "nommer", "tracer"]
        
        if difficulte == "facile":
            type_exercice = "identifier"
            max_coord = 10
            nb_points = 2
        elif difficulte == "moyen":
            type_exercice = random.choice(["identifier", "nommer"])
            max_coord = 15
            nb_points = 3
        else:
            type_exercice = random.choice(types_exercices)
            max_coord = 20
            nb_points = 4
            # ✅ FIX: Obtenir un 4ème point si nécessaire
            if nb_points > 3:
                points_set2 = self._get_next_geometry_points()
                points = points + [points_set2[0]]
        
        # Générer coordonnées
        coords = {}
        for i in range(nb_points):
            point = points[i]
            coords[f"{point}_x"] = random.randint(2, max_coord - 2)
            coords[f"{point}_y"] = random.randint(2, max_coord - 2)
        
        # Construire énoncé selon type
        if type_exercice == "identifier":
            figure_type = random.choice(["segment", "droite", "demi_droite"])
            
            if figure_type == "segment":
                enonce = f"Sur la figure ci-dessous, la figure [{points[0]}{points[1]}] est-elle un segment, une droite ou une demi-droite ?"
                etapes = [
                    f"[{points[0]}{points[1]}] est un segment",
                    f"Un segment est limité par deux points {points[0]} et {points[1]}",
                    f"Il a une longueur mesurable"
                ]
                resultat = "segment"
            elif figure_type == "droite":
                enonce = f"Sur la figure ci-dessous, la figure ({points[0]}{points[1]}) est-elle un segment, une droite ou une demi-droite ?"
                etapes = [
                    f"({points[0]}{points[1]}) est une droite",
                    "Une droite est illimitée des deux côtés",
                    "Elle passe par les points mais n'a pas de longueur finie"
                ]
                resultat = "droite"
            else:
                enonce = f"Sur la figure ci-dessous, la figure [{points[0]}{points[1]}) est-elle un segment, une droite ou une demi-droite ?"
                etapes = [
                    f"[{points[0]}{points[1]}) est une demi-droite",
                    f"Une demi-droite a une origine (point {points[0]}) et est illimitée dans un sens",
                    f"Elle passe par {points[1]} mais continue à l'infini"
                ]
                resultat = "demi-droite"
            
            figure = GeometricFigure(
                type="points_segments_droites",
                points=points[:nb_points],
                longueurs_connues=coords,
                proprietes=["with_grid", figure_type]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "identifier",
                    "enonce": enonce,
                    "figure_type": figure_type,
                    "points": points[:nb_points]
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Identification correcte", "points": 2.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève distingue bien segment/droite/demi-droite",
                    "Insister sur la notation : [AB] segment, (AB) droite, [AB) demi-droite"
                ]
            )
        
        elif type_exercice == "nommer":
            enonce = f"Sur la figure, nommer correctement la droite passant par les points {points[0]} et {points[1]}."
            
            etapes = [
                f"La droite passant par {points[0]} et {points[1]} se note ({points[0]}{points[1]}) ou ({points[1]}{points[0]})",
                "Les deux notations sont équivalentes",
                "On utilise des parenthèses () pour une droite"
            ]
            
            resultat = f"({points[0]}{points[1]})"
            
            figure = GeometricFigure(
                type="points_segments_droites",
                points=points[:nb_points],
                longueurs_connues=coords,
                proprietes=["with_grid", "droite"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "nommer",
                    "enonce": enonce,
                    "points": points[:nb_points]
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Notation correcte", "points": 2.0}
                ]
            )
        
        else:  # tracer
            figure_type = random.choice(["segment", "droite", "demi_droite"])
            
            if figure_type == "segment":
                enonce = f"Tracer le segment [{points[0]}{points[1]}] reliant {points[0]}({coords[f'{points[0]}_x']}, {coords[f'{points[0]}_y']}) et {points[1]}({coords[f'{points[1]}_x']}, {coords[f'{points[1]}_y']})."
                etapes = [
                    f"1. Placer le point {points[0]}({coords[f'{points[0]}_x']}, {coords[f'{points[0]}_y']})",
                    f"2. Placer le point {points[1]}({coords[f'{points[1]}_x']}, {coords[f'{points[1]}_y']})",
                    f"3. Tracer le segment [{points[0]}{points[1]}] avec la règle"
                ]
            elif figure_type == "droite":
                enonce = f"Tracer la droite ({points[0]}{points[1]}) passant par {points[0]}({coords[f'{points[0]}_x']}, {coords[f'{points[0]}_y']}) et {points[1]}({coords[f'{points[1]}_x']}, {coords[f'{points[1]}_y']})."
                etapes = [
                    f"1. Placer le point {points[0]}({coords[f'{points[0]}_x']}, {coords[f'{points[0]}_y']})",
                    f"2. Placer le point {points[1]}({coords[f'{points[1]}_x']}, {coords[f'{points[1]}_y']})",
                    f"3. Tracer la droite ({points[0]}{points[1]}) avec la règle (prolonger des deux côtés)"
                ]
            else:
                enonce = f"Tracer la demi-droite [{points[0]}{points[1]}) d'origine {points[0]}({coords[f'{points[0]}_x']}, {coords[f'{points[0]}_y']}) passant par {points[1]}({coords[f'{points[1]}_x']}, {coords[f'{points[1]}_y']})."
                etapes = [
                    f"1. Placer le point {points[0]}({coords[f'{points[0]}_x']}, {coords[f'{points[0]}_y']})",
                    f"2. Placer le point {points[1]}({coords[f'{points[1]}_x']}, {coords[f'{points[1]}_y']})",
                    f"3. Tracer la demi-droite [{points[0]}{points[1]}) depuis {points[0]} vers {points[1]} et au-delà"
                ]
            
            resultat = f"{figure_type.replace('_', '-')} tracé"
            
            figure = GeometricFigure(
                type="points_segments_droites",
                points=points[:nb_points],
                longueurs_connues=coords,
                proprietes=["with_grid", figure_type, "construction"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "tracer",
                    "enonce": enonce,
                    "figure_type": figure_type,
                    "points": points[:nb_points]
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Placement des points", "points": 1.0},
                    {"etape": "Tracé correct", "points": 1.0}
                ]
            )


    
    def _gen_alignement_milieu(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur alignement et milieu d'un segment (6e_G02)
        
        Concepts :
        - Vérifier si des points sont alignés
        - Calculer les coordonnées du milieu
        - Construire le milieu avec compas/règle
        """
        
        points = self._get_next_geometry_points()
        
        types_exercices = ["verifier_alignement", "trouver_milieu", "construire_milieu"]
        
        if difficulte == "facile":
            type_exercice = "verifier_alignement"
            max_coord = 10
        elif difficulte == "moyen":
            type_exercice = random.choice(["verifier_alignement", "trouver_milieu"])
            max_coord = 15
        else:
            type_exercice = random.choice(types_exercices)
            max_coord = 20
        
        if type_exercice == "verifier_alignement":
            # Générer 3 points alignés ou non
            sont_alignes = random.choice([True, False])
            
            # Points A et B
            ax = random.randint(2, max_coord - 4)
            ay = random.randint(2, max_coord - 4)
            bx = random.randint(ax + 2, max_coord - 2)
            by = random.randint(ay + 2, max_coord - 2)
            
            if sont_alignes:
                # Point C aligné (même coefficient directeur)
                coeff = (by - ay) / (bx - ax)
                cx = random.randint(bx + 1, min(bx + 3, max_coord))
                cy = round(ay + coeff * (cx - ax))
                # S'assurer que cy est dans les limites
                if cy > max_coord:
                    cy = max_coord
                if cy < 2:
                    cy = 2
            else:
                # Point C non aligné
                cx = random.randint(bx + 1, max_coord)
                cy = random.randint(2, max_coord)
                # S'assurer qu'il n'est PAS aligné
                coeff_ab = (by - ay) / (bx - ax) if (bx - ax) != 0 else 999
                coeff_ac = (cy - ay) / (cx - ax) if (cx - ax) != 0 else 999
                if abs(coeff_ab - coeff_ac) < 0.2:
                    cy = cy + 3 if cy + 3 <= max_coord else cy - 3
            
            enonce = f"Les points {points[0]}({ax}, {ay}), {points[1]}({bx}, {by}) et {points[2]}({cx}, {cy}) sont-ils alignés ? Justifier."
            
            if sont_alignes:
                etapes = [
                    f"Calculons les coefficients directeurs :",
                    f"- Droite ({points[0]}{points[1]}) : ({by}-{ay})/({bx}-{ax}) = {by-ay}/{bx-ax} = {round((by-ay)/(bx-ax), 2)}",
                    f"- Droite ({points[1]}{points[2]}) : ({cy}-{by})/({cx}-{bx}) = {cy-by}/{cx-bx} = {round((cy-by)/(cx-bx), 2) if (cx-bx) != 0 else 'infini'}",
                    f"Les coefficients sont égaux (ou proches), donc {points[0]}, {points[1]} et {points[2]} sont alignés."
                ]
                resultat = "Oui, les points sont alignés"
            else:
                coeff_ab_calc = round((by-ay)/(bx-ax), 2) if (bx-ax) != 0 else "infini"
                coeff_ac_calc = round((cy-ay)/(cx-ax), 2) if (cx-ax) != 0 else "infini"
                etapes = [
                    f"Calculons les coefficients directeurs :",
                    f"- Droite ({points[0]}{points[1]}) : ({by}-{ay})/({bx}-{ax}) = {coeff_ab_calc}",
                    f"- Droite ({points[0]}{points[2]}) : ({cy}-{ay})/({cx}-{ax}) = {coeff_ac_calc}",
                    f"Les coefficients sont différents, donc {points[0]}, {points[1]} et {points[2]} ne sont PAS alignés."
                ]
                resultat = "Non, les points ne sont pas alignés"
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy
            }
            
            figure = GeometricFigure(
                type="alignement_milieu",
                points=points[:3],
                longueurs_connues=coords,
                proprietes=["with_grid", "alignement", "verif_alignement"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "verifier_alignement",
                    "enonce": enonce,
                    "points": points[:3],
                    "sont_alignes": sont_alignes
                },
                solution_calculee={"resultat": resultat, "alignes": sont_alignes},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Calcul des coefficients", "points": 1.5},
                    {"etape": "Conclusion correcte", "points": 0.5}
                ]
            )
        
        elif type_exercice == "trouver_milieu":
            # Points A et B
            ax = random.randint(2, max_coord - 4)
            ay = random.randint(2, max_coord - 4)
            bx = random.randint(ax + 2, max_coord - 2)
            by = random.randint(ay + 2, max_coord - 2)
            
            # Milieu M
            mx = (ax + bx) / 2
            my = (ay + by) / 2
            
            enonce = f"Calculer les coordonnées du milieu M du segment [{points[0]}{points[1]}] avec {points[0]}({ax}, {ay}) et {points[1]}({bx}, {by})."
            
            etapes = [
                f"Formule du milieu : M((x_{points[0]}+x_{points[1]})/2, (y_{points[0]}+y_{points[1]})/2)",
                f"M(({ax}+{bx})/2, ({ay}+{by})/2)",
                f"M({mx}, {my})"
            ]
            
            resultat = f"M({mx}, {my})"
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                "M_x": mx,
                "M_y": my
            }
            
            figure = GeometricFigure(
                type="alignement_milieu",
                points=points[:2] + ["M"],
                longueurs_connues=coords,
                proprietes=["with_grid", "milieu", "segment"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_milieu",
                    "enonce": enonce,
                    "points": points[:2],
                    "ax": ax, "ay": ay,
                    "bx": bx, "by": by
                },
                solution_calculee={"mx": mx, "my": my, "resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Application de la formule", "points": 1.0},
                    {"etape": "Calcul correct", "points": 1.0}
                ]
            )
        
        else:  # construire_milieu
            # Points A et B
            ax = random.randint(2, max_coord - 4)
            ay = random.randint(2, max_coord - 4)
            bx = random.randint(ax + 3, max_coord - 2)
            by = random.randint(ay + 3, max_coord - 2)
            
            # Milieu M (pour référence)
            mx = (ax + bx) / 2
            my = (ay + by) / 2
            
            enonce = f"Construire le milieu M du segment [{points[0]}{points[1]}] avec {points[0]}({ax}, {ay}) et {points[1]}({bx}, {by}) en utilisant la règle et le compas."
            
            etapes = [
                f"1. Tracer le segment [{points[0]}{points[1]}]",
                f"2. Avec le compas, tracer un cercle de centre {points[0]} de rayon [{points[0]}{points[1]}]",
                f"3. Avec le compas, tracer un cercle de centre {points[1]} de même rayon",
                "4. Les deux cercles se coupent en deux points",
                "5. La droite passant par ces deux points coupe [AB] en son milieu M",
                f"6. Le milieu M a pour coordonnées ({mx}, {my})"
            ]
            
            resultat = f"Milieu M({mx}, {my}) construit"
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                "M_x": mx,
                "M_y": my
            }
            
            figure = GeometricFigure(
                type="alignement_milieu",
                points=points[:2] + ["M"],
                longueurs_connues=coords,
                proprietes=["with_grid", "milieu", "construction", "compas"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "construire_milieu",
                    "enonce": enonce,
                    "points": points[:2]
                },
                solution_calculee={"mx": mx, "my": my, "resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Construction des cercles", "points": 1.0},
                    {"etape": "Tracé de la médiatrice", "points": 0.5},
                    {"etape": "Placement du milieu", "points": 0.5}
                ],
                conseils_prof=[
                    "Vérifier que les cercles ont le même rayon",
                    "S'assurer que la médiatrice est bien perpendiculaire"
                ]
            )


    
    def _nombre_en_lettres(self, nombre: int) -> str:
        """Helper pour convertir un nombre en lettres (simplifié pour 6e)"""
        unites = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
        dizaines_spec = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
        dizaines = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingt", "quatre-vingt-dix"]
        
        if nombre == 0:
            return "zéro"
        
        if nombre < 10:
            return unites[nombre]
        
        if nombre < 20:
            return dizaines_spec[nombre - 10]
        
        if nombre < 100:
            d, u = divmod(nombre, 10)
            if u == 0:
                result = dizaines[d]
                if d == 8:
                    result += "s"  # quatre-vingts
                return result
            elif d == 7 or d == 9:
                return dizaines[d - 1] + "-" + dizaines_spec[u]
            elif u == 1 and d != 8:
                return dizaines[d] + " et un"
            else:
                return dizaines[d] + "-" + unites[u]
        
        if nombre < 1000:
            c, reste = divmod(nombre, 100)
            if c == 1:
                result = "cent"
            else:
                result = unites[c] + " cent"
                if reste == 0:
                    result += "s"
            if reste > 0:
                result += " " + self._nombre_en_lettres(reste)
            return result
        
        if nombre < 1000000:
            m, reste = divmod(nombre, 1000)
            if m == 1:
                result = "mille"
            else:
                result = self._nombre_en_lettres(m) + " mille"
            if reste > 0:
                result += " " + self._nombre_en_lettres(reste)
            return result
        
        return str(nombre)  # Fallback pour nombres très grands
    
    def _gen_lire_ecrire_entiers(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur lire et écrire les nombres entiers (6e_N01)
        
        Concepts :
        - Lire un nombre en lettres → chiffres
        - Écrire un nombre en chiffres → lettres
        - Décomposer un nombre
        """
        
        types_exercices = ["lire_nombre", "ecrire_nombre", "decomposer"]
        
        if difficulte == "facile":
            type_exercice = "lire_nombre"
            nombre = random.randint(1, 100)
        elif difficulte == "moyen":
            type_exercice = random.choice(["lire_nombre", "ecrire_nombre"])
            nombre = random.randint(100, 10000)
        else:
            type_exercice = random.choice(types_exercices)
            nombre = random.randint(10000, 100000)
        
        if type_exercice == "lire_nombre":
            # Convertir nombre en lettres
            nombre_lettres = self._nombre_en_lettres(nombre)
            enonce = f"Écrire en chiffres : {nombre_lettres}"
            resultat = str(nombre)
            etapes = [f"{nombre_lettres} = {nombre}"]
        
        elif type_exercice == "ecrire_nombre":
            # Convertir nombre en lettres
            nombre_lettres = self._nombre_en_lettres(nombre)
            
            # Formater avec espaces pour nombres > 999
            if nombre > 999:
                nombre_formate = f"{nombre:,}".replace(",", " ")
            else:
                nombre_formate = str(nombre)
            
            enonce = f"Écrire en lettres : {nombre_formate}"
            resultat = nombre_lettres
            etapes = [f"{nombre} = {nombre_lettres}"]
        
        else:  # decomposer
            # Formater avec espaces pour nombres > 999
            if nombre > 999:
                nombre_formate = f"{nombre:,}".replace(",", " ")
            else:
                nombre_formate = str(nombre)
            
            enonce = f"Décomposer le nombre {nombre_formate} selon les unités, dizaines, centaines, etc."
            
            # Décomposition
            decomposition_parts = []
            decomposition_additive = []
            
            chiffres = str(nombre)
            longueur = len(chiffres)
            
            for i, chiffre in enumerate(chiffres):
                if chiffre != '0':
                    valeur_position = int(chiffre) * (10 ** (longueur - i - 1))
                    decomposition_parts.append(f"{chiffre} × {10 ** (longueur - i - 1)}")
                    decomposition_additive.append(str(valeur_position))
            
            etapes = [
                f"{nombre} = " + " + ".join(decomposition_parts),
                f"{nombre} = " + " + ".join(decomposition_additive)
            ]
            
            resultat = " + ".join(decomposition_additive)
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.CALCUL_DECIMAUX,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "type": type_exercice,
                "enonce": enonce,
                "nombre": nombre
            },
            solution_calculee={"resultat": resultat},
            etapes_calculees=etapes,
            resultat_final=str(resultat),
            figure_geometrique=None,
            points_bareme=[
                {"etape": "Conversion/Décomposition correcte", "points": 2.0}
            ],
            conseils_prof=[
                "Vérifier la bonne écriture des nombres",
                "Insister sur les règles d'orthographe (trait d'union, 's' à vingt et cent)"
            ]
        )


    
    def _gen_comparer_ranger_entiers(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur comparer et ranger les nombres entiers (6e_N02)
        
        Concepts :
        - Comparer deux nombres (>, <, =)
        - Ranger plusieurs nombres
        - Encadrer un nombre
        """
        
        types_exercices = ["comparer", "ranger", "encadrer"]
        
        if difficulte == "facile":
            type_exercice = "comparer"
            nombres = [random.randint(1, 100) for _ in range(2)]
        elif difficulte == "moyen":
            type_exercice = random.choice(["comparer", "ranger"])
            nombres = [random.randint(100, 1000) for _ in range(random.randint(3, 4))]
        else:
            type_exercice = random.choice(types_exercices)
            nombres = [random.randint(1000, 10000) for _ in range(random.randint(4, 5))]
        
        if type_exercice == "comparer":
            a, b = nombres[0], nombres[1]
            enonce = f"Comparer les nombres {a} et {b}. Utiliser le symbole <, > ou =."
            
            if a > b:
                symbole = ">"
                resultat = f"{a} > {b}"
                etapes = [
                    f"{a} > {b}",
                    f"Le nombre {a} est plus grand que {b}."
                ]
            elif a < b:
                symbole = "<"
                resultat = f"{a} < {b}"
                etapes = [
                    f"{a} < {b}",
                    f"Le nombre {b} est plus grand que {a}."
                ]
            else:
                symbole = "="
                resultat = f"{a} = {b}"
                etapes = [
                    f"{a} = {b}",
                    "Les deux nombres sont égaux."
                ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "comparer",
                    "enonce": enonce,
                    "a": a,
                    "b": b
                },
                solution_calculee={"resultat": resultat, "symbole": symbole},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Comparaison correcte", "points": 2.0}
                ]
            )
        
        elif type_exercice == "ranger":
            ordre = random.choice(["croissant", "décroissant"])
            enonce = f"Ranger les nombres {', '.join(map(str, nombres))} dans l'ordre {ordre}."
            
            if ordre == "croissant":
                nombres_tries = sorted(nombres)
                resultat = ", ".join(map(str, nombres_tries))
                symbole_ordre = " < "
            else:
                nombres_tries = sorted(nombres, reverse=True)
                resultat = ", ".join(map(str, nombres_tries))
                symbole_ordre = " > "
            
            etapes = [
                f"Ordre {ordre} : {symbole_ordre.join(map(str, nombres_tries))}",
                f"Réponse : {resultat}"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "ranger",
                    "enonce": enonce,
                    "nombres": nombres,
                    "ordre": ordre
                },
                solution_calculee={"resultat": resultat, "nombres_tries": nombres_tries},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Ordre correct", "points": 2.0}
                ]
            )
        
        else:  # encadrer
            nombre = random.choice(nombres)
            
            # Encadrer entre deux centaines ou milliers selon la difficulté
            if difficulte == "moyen":
                # Encadrer entre deux centaines
                centaine_inf = (nombre // 100) * 100
                centaine_sup = centaine_inf + 100
                enonce = f"Encadrer le nombre {nombre} entre deux centaines consécutives."
                resultat = f"{centaine_inf} < {nombre} < {centaine_sup}"
                etapes = [
                    f"{nombre} est entre {centaine_inf} et {centaine_sup}",
                    f"{centaine_inf} < {nombre} < {centaine_sup}"
                ]
            else:
                # Encadrer entre deux milliers
                millier_inf = (nombre // 1000) * 1000
                millier_sup = millier_inf + 1000
                enonce = f"Encadrer le nombre {nombre} entre deux milliers consécutifs."
                resultat = f"{millier_inf} < {nombre} < {millier_sup}"
                etapes = [
                    f"{nombre} est entre {millier_inf} et {millier_sup}",
                    f"{millier_inf} < {nombre} < {millier_sup}"
                ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "encadrer",
                    "enonce": enonce,
                    "nombre": nombre
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Encadrement correct", "points": 2.0}
                ],
                conseils_prof=[
                    "Vérifier que l'encadrement est bien entre deux valeurs consécutives",
                    "Insister sur l'utilisation des symboles < et >"
                ]
            )


    
    def _gen_addition_soustraction_entiers(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur addition et soustraction de nombres entiers (6e_N04)
        
        Concepts :
        - Calculer une addition/soustraction
        - Poser l'opération en colonnes
        - Résoudre un problème rédigé
        """
        
        types_exercices = ["calculer", "poser_operation", "probleme"]
        
        if difficulte == "facile":
            type_exercice = "calculer"
            # Nombres sans retenue
            a = random.randint(10, 40)
            b = random.randint(10, 40)
            # Ajuster pour éviter retenue en addition
            if (a % 10) + (b % 10) >= 10:
                b = b - ((a % 10) + (b % 10) - 9)
        elif difficulte == "moyen":
            type_exercice = random.choice(["calculer", "poser_operation"])
            a = random.randint(50, 200)
            b = random.randint(50, 200)
        else:
            type_exercice = random.choice(types_exercices)
            a = random.randint(200, 1000)
            b = random.randint(200, 1000)
        
        operation = random.choice(["+", "-"])
        
        # Pour la soustraction, s'assurer que a > b
        if operation == "-" and a < b:
            a, b = b, a
        
        if type_exercice == "calculer":
            if operation == "+":
                enonce = f"Effectuer l'addition : {a} + {b}"
                resultat = a + b
                etapes = [f"{a} + {b} = {resultat}"]
            else:
                enonce = f"Effectuer la soustraction : {a} - {b}"
                resultat = a - b
                etapes = [f"{a} - {b} = {resultat}"]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_RELATIFS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer",
                    "enonce": enonce,
                    "operation": operation,
                    "a": a,
                    "b": b
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=str(resultat),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Calcul correct", "points": 2.0}
                ]
            )
        
        elif type_exercice == "poser_operation":
            enonce = f"Poser et calculer : {a} {operation} {b}"
            
            if operation == "+":
                resultat = a + b
                # Détailler les étapes de l'addition en colonnes
                etapes = [
                    f"  {a}",
                    f"{operation} {b}",
                    "-----",
                    f"  {resultat}",
                    "",
                    "Calcul par colonne (de droite à gauche) :"
                ]
                
                # Détail unités, dizaines, centaines...
                str_a = str(a)
                str_b = str(b)
                str_r = str(resultat)
                
                # Unités
                u_a = int(str_a[-1]) if len(str_a) >= 1 else 0
                u_b = int(str_b[-1]) if len(str_b) >= 1 else 0
                u_sum = u_a + u_b
                retenue_u = u_sum // 10
                u_r = u_sum % 10
                
                if retenue_u > 0:
                    etapes.append(f"Unités : {u_a} + {u_b} = {u_sum}, on pose {u_r} et on retient {retenue_u}")
                else:
                    etapes.append(f"Unités : {u_a} + {u_b} = {u_r}")
                
                # Dizaines (si nécessaire)
                if len(str_a) >= 2 or len(str_b) >= 2:
                    d_a = int(str_a[-2]) if len(str_a) >= 2 else 0
                    d_b = int(str_b[-2]) if len(str_b) >= 2 else 0
                    d_sum = d_a + d_b + retenue_u
                    retenue_d = d_sum // 10
                    d_r = d_sum % 10
                    
                    if retenue_d > 0:
                        etapes.append(f"Dizaines : {d_a} + {d_b} + {retenue_u} = {d_sum}, on pose {d_r} et on retient {retenue_d}")
                    else:
                        etapes.append(f"Dizaines : {d_a} + {d_b} + {retenue_u} = {d_r}")
                
                etapes.append(f"Résultat : {resultat}")
            else:
                resultat = a - b
                etapes = [
                    f"  {a}",
                    f"- {b}",
                    "-----",
                    f"  {resultat}"
                ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_RELATIFS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "poser_operation",
                    "enonce": enonce,
                    "operation": operation,
                    "a": a,
                    "b": b
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=str(resultat),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Opération posée correctement", "points": 0.5},
                    {"etape": "Calcul correct", "points": 1.5}
                ]
            )
        
        else:  # probleme
            themes = [
                {"nom": "argent", "unite": "€", "contexte_add": "reçoit", "contexte_sub": "dépense"},
                {"nom": "objets", "unite": "objets", "contexte_add": "achète", "contexte_sub": "donne"},
                {"nom": "distance", "unite": "km", "contexte_add": "parcourt en plus", "contexte_sub": "parcourt en moins"}
            ]
            
            theme = random.choice(themes)
            
            if operation == "+":
                enonce = f"Marie a {a} {theme['unite']}. Elle {theme['contexte_add']} {b} {theme['unite']}. Combien a-t-elle maintenant ?"
                resultat = a + b
                etapes = [
                    f"{a} + {b} = {resultat}",
                    f"Marie a maintenant {resultat} {theme['unite']}."
                ]
            else:
                enonce = f"Marie a {a} {theme['unite']}. Elle {theme['contexte_sub']} {b} {theme['unite']}. Combien lui reste-t-il ?"
                resultat = a - b
                etapes = [
                    f"{a} - {b} = {resultat}",
                    f"Il reste {resultat} {theme['unite']} à Marie."
                ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_RELATIFS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "probleme",
                    "enonce": enonce,
                    "operation": operation,
                    "a": a,
                    "b": b,
                    "theme": theme["nom"]
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=f"{resultat} {theme['unite']}",
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Compréhension du problème", "points": 0.5},
                    {"etape": "Opération correcte", "points": 1.0},
                    {"etape": "Résultat avec unité", "points": 0.5}
                ],
                conseils_prof=[
                    "Vérifier que l'élève comprend bien la situation",
                    "S'assurer qu'il choisit la bonne opération",
                    "Insister sur l'importance de l'unité dans la réponse"
                ]
            )


    
    # ============================================================================
    # SPRINT 3 - GÉNÉRATEURS 6e (G04, G05, N05, N06, N07)
    # ============================================================================
    
    def _gen_triangles(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur les triangles (6e_G04)
        
        Concepts :
        - Classer un triangle (équilatéral, isocèle, quelconque)
        - Construire un triangle
        - Vérifier propriétés (somme angles = 180°, inégalité triangulaire)
        """
        
        points = self._get_next_geometry_points()
        
        types_exercices = ["classer", "construire", "verifier_propriete"]
        
        if difficulte == "facile":
            type_exercice = "classer"
            max_coord = 10
        elif difficulte == "moyen":
            type_exercice = "construire"
            max_coord = 15
        else:
            type_exercice = "verifier_propriete"
            max_coord = 20
        
        if type_exercice == "classer":
            # Générer 3 longueurs de côtés
            type_triangle = random.choice(["equilateral", "isocele", "quelconque"])
            
            if type_triangle == "equilateral":
                cote = random.randint(4, 10)
                ab = bc = ca = cote
                classification = "équilatéral (3 côtés égaux)"
            elif type_triangle == "isocele":
                cote_egal = random.randint(5, 10)
                cote_diff = random.randint(3, cote_egal - 1) if cote_egal > 3 else random.randint(cote_egal + 1, 12)
                
                # Vérifier l'inégalité triangulaire : la somme de deux côtés doit être > au 3ème
                if cote_egal + cote_diff <= cote_egal:
                    cote_diff = cote_egal - 2 if cote_egal > 2 else cote_egal + 2
                
                ab = bc = cote_egal
                ca = cote_diff
                classification = "isocèle (2 côtés égaux)"
            else:  # quelconque
                ab = random.randint(4, 8)
                bc = random.randint(5, 9)
                ca = random.randint(6, 10)
                
                # S'assurer que c'est vraiment quelconque
                if ab == bc or bc == ca or ab == ca:
                    ca = ab + bc - 1
                
                # Vérifier l'inégalité triangulaire
                if ab + bc <= ca:
                    ca = ab + bc - 1
                if ab + ca <= bc:
                    bc = ab + ca - 1
                if bc + ca <= ab:
                    ab = bc + ca - 1
                
                classification = "quelconque (3 côtés différents)"
            
            enonce = f"Classer le triangle {points[0]}{points[1]}{points[2]} selon ses côtés. Les côtés mesurent : {points[0]}{points[1]} = {ab} cm, {points[1]}{points[2]} = {bc} cm, {points[0]}{points[2]} = {ca} cm."
            
            etapes = [
                f"{points[0]}{points[1]} = {ab} cm, {points[1]}{points[2]} = {bc} cm, {points[0]}{points[2]} = {ca} cm"
            ]
            
            if type_triangle == "equilateral":
                etapes.append(f"Les 3 côtés sont égaux : {ab} = {bc} = {ca}")
                etapes.append(f"Le triangle {points[0]}{points[1]}{points[2]} est {classification}")
            elif type_triangle == "isocele":
                etapes.append(f"Deux côtés sont égaux : {points[0]}{points[1]} = {points[1]}{points[2]} = {cote_egal} cm")
                etapes.append(f"Le triangle {points[0]}{points[1]}{points[2]} est {classification}")
            else:
                etapes.append(f"Les 3 côtés sont différents")
                etapes.append(f"Le triangle {points[0]}{points[1]}{points[2]} est {classification}")
            
            resultat = f"Triangle {classification}"
            
            # Coordonnées pour le schéma
            ax, ay = random.randint(2, max_coord - 4), random.randint(2, max_coord - 4)
            bx = ax + ab
            by = ay
            
            # Calculer C avec la loi des cosinus (approximation simple)
            import math
            angle = math.radians(60)  # Angle arbitraire pour visualisation
            cx = ax + ca * math.cos(angle)
            cy = ay + ca * math.sin(angle)
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": int(cx),
                f"{points[2]}_y": int(cy)
            }
            
            figure = GeometricFigure(
                type="triangle",
                points=points[:3],
                longueurs_connues=coords,
                proprietes=["with_grid", "triangle", type_triangle]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "classer",
                    "enonce": enonce,
                    "type_triangle": type_triangle,
                    "ab": ab, "bc": bc, "ca": ca
                },
                solution_calculee={"resultat": resultat, "type": type_triangle},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Identification des mesures", "points": 0.5},
                    {"etape": "Classification correcte", "points": 1.5}
                ]
            )
        
        elif type_exercice == "construire":
            # Construire un triangle avec 3 points donnés
            ax = random.randint(2, max_coord - 4)
            ay = random.randint(2, max_coord - 4)
            bx = random.randint(ax + 3, max_coord - 2)
            by = random.randint(ay - 2, ay + 2)
            cx = random.randint(ax + 1, max_coord - 2)
            cy = random.randint(ay + 3, max_coord)
            
            # Calculer les longueurs
            import math
            ab = round(math.sqrt((bx - ax)**2 + (by - ay)**2), 1)
            bc = round(math.sqrt((cx - bx)**2 + (cy - by)**2), 1)
            ca = round(math.sqrt((ax - cx)**2 + (ay - cy)**2), 1)
            
            enonce = f"Construire le triangle {points[0]}{points[1]}{points[2]} avec les coordonnées : {points[0]}({ax}, {ay}), {points[1]}({bx}, {by}), {points[2]}({cx}, {cy})."
            
            etapes = [
                f"1. Placer le point {points[0]}({ax}, {ay})",
                f"2. Placer le point {points[1]}({bx}, {by})",
                f"3. Placer le point {points[2]}({cx}, {cy})",
                f"4. Tracer les segments [{points[0]}{points[1]}], [{points[1]}{points[2]}], et [{points[2]}{points[0]}]",
                f"Le triangle a pour côtés : {points[0]}{points[1]} ≈ {ab} cm, {points[1]}{points[2]} ≈ {bc} cm, {points[2]}{points[0]} ≈ {ca} cm"
            ]
            
            resultat = f"Triangle {points[0]}{points[1]}{points[2]} construit"
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy
            }
            
            figure = GeometricFigure(
                type="triangle",
                points=points[:3],
                longueurs_connues=coords,
                proprietes=["with_grid", "triangle", "construction"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "construire",
                    "enonce": enonce,
                    "points": points[:3]
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Placement des points", "points": 1.0},
                    {"etape": "Tracé des segments", "points": 1.0}
                ]
            )
        
        else:  # verifier_propriete
            # Vérifier la somme des angles ou l'inégalité triangulaire
            propriete = random.choice(["somme_angles", "inegalite_triangulaire"])
            
            if propriete == "somme_angles":
                # Générer 2 angles, calculer le 3ème
                angle_a = random.randint(40, 80)
                angle_b = random.randint(40, 80)
                angle_c = 180 - angle_a - angle_b
                
                # S'assurer que tous les angles sont positifs
                if angle_c <= 0:
                    angle_a = random.randint(40, 60)
                    angle_b = random.randint(40, 60)
                    angle_c = 180 - angle_a - angle_b
                
                enonce = f"Dans le triangle {points[0]}{points[1]}{points[2]}, on connaît deux angles : angle en {points[0]} = {angle_a}° et angle en {points[1]} = {angle_b}°. Calculer l'angle en {points[2]}."
                
                etapes = [
                    "Dans un triangle, la somme des angles vaut toujours 180°",
                    f"angle {points[0]} + angle {points[1]} + angle {points[2]} = 180°",
                    f"{angle_a}° + {angle_b}° + angle {points[2]} = 180°",
                    f"angle {points[2]} = 180° - {angle_a}° - {angle_b}°",
                    f"angle {points[2]} = {angle_c}°"
                ]
                
                resultat = f"{angle_c}°"
                
            else:  # inegalite_triangulaire
                # Vérifier si 3 longueurs peuvent former un triangle
                peut_former = random.choice([True, False])
                
                if peut_former:
                    a = random.randint(4, 10)
                    b = random.randint(4, 10)
                    c = random.randint(max(abs(a - b) + 1, 3), a + b - 1)
                else:
                    a = random.randint(5, 10)
                    b = random.randint(3, 7)
                    c = a + b + 2  # Viole l'inégalité
                
                enonce = f"Peut-on construire un triangle avec des côtés de longueurs {a} cm, {b} cm et {c} cm ? Justifier avec l'inégalité triangulaire."
                
                etapes = [
                    "Inégalité triangulaire : la somme de deux côtés doit être strictement supérieure au troisième",
                    f"Vérification 1 : {a} + {b} = {a + b} {'>' if a + b > c else '<='} {c}",
                    f"Vérification 2 : {a} + {c} = {a + c} {'>' if a + c > b else '<='} {b}",
                    f"Vérification 3 : {b} + {c} = {b + c} {'>' if b + c > a else '<='} {a}"
                ]
                
                if peut_former:
                    etapes.append(f"Toutes les inégalités sont vérifiées, donc OUI, on peut construire un triangle.")
                    resultat = "Oui, le triangle peut être construit"
                else:
                    etapes.append(f"Au moins une inégalité n'est pas vérifiée, donc NON, on ne peut pas construire un triangle.")
                    resultat = "Non, le triangle ne peut pas être construit"
            
            # Schéma simple pour visualisation
            ax, ay = 3, 3
            bx, by = 10, 3
            cx, cy = 6, 8
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy
            }
            
            figure = GeometricFigure(
                type="triangle",
                points=points[:3],
                longueurs_connues=coords,
                proprietes=["with_grid", "triangle", propriete]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.TRIANGLE_QUELCONQUE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "verifier_propriete",
                    "enonce": enonce,
                    "propriete": propriete
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Application de la propriété", "points": 1.0},
                    {"etape": "Calcul/Vérification correcte", "points": 1.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève connaît bien la propriété utilisée",
                    "S'assurer de la rigueur dans les calculs"
                ]
            )


    
    def _gen_quadrilateres(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur les quadrilatères usuels (6e_G05)
        
        Concepts :
        - Identifier carré, rectangle, losange, parallélogramme
        - Construire un quadrilatère
        - Vérifier propriétés (angles, côtés parallèles)
        """
        
        points = self._get_next_geometry_points()
        # Besoin de 4 points pour un quadrilatère
        points_set2 = self._get_next_geometry_points()
        points = points + [points_set2[0]]
        
        types_exercices = ["identifier", "construire", "verifier_propriete"]
        
        if difficulte == "facile":
            type_exercice = "identifier"
            max_coord = 10
        elif difficulte == "moyen":
            type_exercice = "construire"
            max_coord = 15
        else:
            type_exercice = "verifier_propriete"
            max_coord = 20
        
        if type_exercice == "identifier":
            # Identifier le type de quadrilatère
            type_quad = random.choice(["carre", "rectangle", "losange", "parallelogramme"])
            
            if type_quad == "carre":
                cote = random.randint(4, 8)
                ab = bc = cd = da = cote
                description = "carré (4 côtés égaux et 4 angles droits)"
            elif type_quad == "rectangle":
                longueur = random.randint(6, 10)
                largeur = random.randint(3, 5)
                ab = cd = longueur
                bc = da = largeur
                description = "rectangle (côtés opposés égaux et 4 angles droits)"
            elif type_quad == "losange":
                cote = random.randint(5, 9)
                ab = bc = cd = da = cote
                description = "losange (4 côtés égaux)"
            else:  # parallelogramme
                cote1 = random.randint(6, 10)
                cote2 = random.randint(4, 7)
                ab = cd = cote1
                bc = da = cote2
                description = "parallélogramme (côtés opposés égaux et parallèles)"
            
            enonce = f"Identifier le quadrilatère {points[0]}{points[1]}{points[2]}{points[3]} sachant que : {points[0]}{points[1]} = {ab} cm, {points[1]}{points[2]} = {bc} cm, {points[2]}{points[3]} = {cd} cm, {points[3]}{points[0]} = {da} cm."
            
            if type_quad == "carre":
                enonce += f" Tous les angles sont droits."
            elif type_quad == "rectangle":
                enonce += f" Tous les angles sont droits."
            
            etapes = [
                f"Côtés : {points[0]}{points[1]} = {ab} cm, {points[1]}{points[2]} = {bc} cm, {points[2]}{points[3]} = {cd} cm, {points[3]}{points[0]} = {da} cm"
            ]
            
            if type_quad == "carre":
                etapes.append("Les 4 côtés sont égaux et les 4 angles sont droits")
                etapes.append(f"Le quadrilatère est un {description}")
            elif type_quad == "rectangle":
                etapes.append("Les côtés opposés sont égaux et les 4 angles sont droits")
                etapes.append(f"Le quadrilatère est un {description}")
            elif type_quad == "losange":
                etapes.append("Les 4 côtés sont égaux")
                etapes.append(f"Le quadrilatère est un {description}")
            else:
                etapes.append("Les côtés opposés sont égaux")
                etapes.append(f"Le quadrilatère est un {description}")
            
            resultat = description
            
            # Coordonnées pour le schéma
            ax, ay = 2, 2
            bx = ax + ab
            by = ay
            cx, cy = bx, by + bc
            dx = ax
            dy = cy
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy,
                f"{points[3]}_x": dx,
                f"{points[3]}_y": dy
            }
            
            figure = GeometricFigure(
                type="quadrilatere",
                points=points[:4],
                longueurs_connues=coords,
                proprietes=["with_grid", "quadrilatere", type_quad]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.RECTANGLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "identifier",
                    "enonce": enonce,
                    "type_quad": type_quad,
                    "ab": ab, "bc": bc, "cd": cd, "da": da
                },
                solution_calculee={"resultat": resultat, "type": type_quad},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Analyse des mesures", "points": 0.5},
                    {"etape": "Identification correcte", "points": 1.5}
                ]
            )
        
        elif type_exercice == "construire":
            # Construire un quadrilatère spécifique
            type_quad = random.choice(["rectangle", "carre"])
            
            if type_quad == "carre":
                cote = random.randint(4, 8)
                enonce = f"Construire un carré {points[0]}{points[1]}{points[2]}{points[3]} de côté {cote} cm."
                
                etapes = [
                    f"1. Tracer le segment [{points[0]}{points[1]}] de {cote} cm",
                    f"2. En {points[1]}, tracer la perpendiculaire à [{points[0]}{points[1]}]",
                    f"3. Placer {points[2]} à {cote} cm de {points[1]} sur cette perpendiculaire",
                    f"4. Compléter le carré en traçant les côtés [{points[2]}{points[3]}] et [{points[3]}{points[0]}]",
                    "Vérifier : les 4 côtés mesurent la même longueur et les 4 angles sont droits"
                ]
                
                resultat = f"Carré de côté {cote} cm construit"
                
                # Coordonnées
                ax, ay = 2, 2
                bx, by = ax + cote, ay
                cx, cy = bx, by + cote
                dx, dy = ax, cy
            else:  # rectangle
                longueur = random.randint(6, 10)
                largeur = random.randint(3, 5)
                
                enonce = f"Construire un rectangle {points[0]}{points[1]}{points[2]}{points[3]} avec {points[0]}{points[1]} = {longueur} cm et {points[1]}{points[2]} = {largeur} cm."
                
                etapes = [
                    f"1. Tracer le segment [{points[0]}{points[1]}] de {longueur} cm",
                    f"2. En {points[1]}, tracer la perpendiculaire à [{points[0]}{points[1]}]",
                    f"3. Placer {points[2]} à {largeur} cm de {points[1]} sur cette perpendiculaire",
                    f"4. Tracer [{points[2]}{points[3]}] parallèle à [{points[0]}{points[1]}] de longueur {longueur} cm",
                    f"5. Relier {points[3]} à {points[0]}",
                    "Vérifier : les côtés opposés sont égaux et les 4 angles sont droits"
                ]
                
                resultat = f"Rectangle {longueur} cm × {largeur} cm construit"
                
                # Coordonnées
                ax, ay = 2, 2
                bx, by = ax + longueur, ay
                cx, cy = bx, by + largeur
                dx, dy = ax, cy
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy,
                f"{points[3]}_x": dx,
                f"{points[3]}_y": dy
            }
            
            figure = GeometricFigure(
                type="quadrilatere",
                points=points[:4],
                longueurs_connues=coords,
                proprietes=["with_grid", "quadrilatere", type_quad, "construction"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.RECTANGLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "construire",
                    "enonce": enonce,
                    "type_quad": type_quad
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Tracé du premier côté", "points": 0.5},
                    {"etape": "Perpendiculaires/parallèles", "points": 0.75},
                    {"etape": "Complétion du quadrilatère", "points": 0.75}
                ]
            )
        
        else:  # verifier_propriete
            # Vérifier une propriété (angles droits, côtés parallèles)
            propriete = random.choice(["angles_droits", "cotes_paralleles"])
            
            if propriete == "angles_droits":
                # Vérifier si un quadrilatère a des angles droits
                a_angles_droits = random.choice([True, False])
                
                if a_angles_droits:
                    angle_a = angle_b = angle_c = angle_d = 90
                    enonce = f"Le quadrilatère {points[0]}{points[1]}{points[2]}{points[3]} a les angles suivants : angle en {points[0]} = {angle_a}°, angle en {points[1]} = {angle_b}°, angle en {points[2]} = {angle_c}°, angle en {points[3]} = {angle_d}°. Ce quadrilatère a-t-il tous ses angles droits ?"
                    
                    etapes = [
                        f"Tous les angles valent 90° : {angle_a}° = {angle_b}° = {angle_c}° = {angle_d}° = 90°",
                        "Donc OUI, le quadrilatère a tous ses angles droits"
                    ]
                    resultat = "Oui, tous les angles sont droits"
                else:
                    angle_a = 90
                    angle_b = 90
                    angle_c = random.randint(85, 95)
                    angle_d = 360 - angle_a - angle_b - angle_c
                    
                    enonce = f"Le quadrilatère {points[0]}{points[1]}{points[2]}{points[3]} a les angles suivants : angle en {points[0]} = {angle_a}°, angle en {points[1]} = {angle_b}°, angle en {points[2]} = {angle_c}°, angle en {points[3]} = {angle_d}°. Ce quadrilatère a-t-il tous ses angles droits ?"
                    
                    etapes = [
                        f"Angles : {angle_a}°, {angle_b}°, {angle_c}°, {angle_d}°",
                        f"L'angle en {points[2]} vaut {angle_c}° ≠ 90°",
                        "Donc NON, le quadrilatère n'a pas tous ses angles droits"
                    ]
                    resultat = "Non, tous les angles ne sont pas droits"
            
            else:  # cotes_paralleles
                # Vérifier si les côtés opposés sont parallèles
                sont_paralleles = random.choice([True, False])
                
                if sont_paralleles:
                    enonce = f"Dans le quadrilatère {points[0]}{points[1]}{points[2]}{points[3]}, les côtés [{points[0]}{points[1]}] et [{points[3]}{points[2]}] sont-ils parallèles ? On sait que les deux côtés ont la même pente."
                    
                    etapes = [
                        "Deux droites sont parallèles si elles ont la même pente (coefficient directeur)",
                        f"Les côtés [{points[0]}{points[1]}] et [{points[3]}{points[2]}] ont la même pente",
                        "Donc OUI, les côtés sont parallèles"
                    ]
                    resultat = "Oui, les côtés sont parallèles"
                else:
                    enonce = f"Dans le quadrilatère {points[0]}{points[1]}{points[2]}{points[3]}, les côtés [{points[0]}{points[1]}] et [{points[3]}{points[2]}] sont-ils parallèles ? Les pentes sont différentes."
                    
                    etapes = [
                        "Deux droites sont parallèles si elles ont la même pente",
                        f"Les côtés [{points[0]}{points[1]}] et [{points[3]}{points[2]}] ont des pentes différentes",
                        "Donc NON, les côtés ne sont pas parallèles"
                    ]
                    resultat = "Non, les côtés ne sont pas parallèles"
            
            # Coordonnées simples pour visualisation
            ax, ay = 2, 2
            bx, by = 8, 2
            cx, cy = 8, 6
            dx, dy = 2, 6
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy,
                f"{points[3]}_x": dx,
                f"{points[3]}_y": dy
            }
            
            figure = GeometricFigure(
                type="quadrilatere",
                points=points[:4],
                longueurs_connues=coords,
                proprietes=["with_grid", "quadrilatere", propriete]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.RECTANGLE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "verifier_propriete",
                    "enonce": enonce,
                    "propriete": propriete
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Application de la propriété", "points": 1.0},
                    {"etape": "Conclusion correcte", "points": 1.0}
                ],
                conseils_prof=[
                    "Insister sur les propriétés caractéristiques des quadrilatères",
                    "Vérifier que l'élève sait distinguer les différents types"
                ]
            )


    
    def _gen_multiplication_entiers(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur la multiplication de nombres entiers (6e_N05)
        
        Concepts :
        - Calculer une multiplication simple
        - Poser une multiplication en colonnes
        - Résoudre des problèmes contextuels
        """
        
        types_exercices = ["calculer", "poser_operation", "probleme"]
        
        if difficulte == "facile":
            type_exercice = "calculer"
            a = random.randint(2, 20)
            b = random.randint(2, 10)
        elif difficulte == "moyen":
            type_exercice = random.choice(["calculer", "poser_operation"])
            a = random.randint(50, 200)
            b = random.randint(10, 50)
        else:
            type_exercice = random.choice(types_exercices)
            a = random.randint(200, 1000)
            b = random.randint(10, 100)
        
        if type_exercice == "calculer":
            enonce = f"Effectuer la multiplication : {a} × {b}"
            
            resultat = a * b
            etapes = [f"{a} × {b} = {resultat}"]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer",
                    "enonce": enonce,
                    "a": a,
                    "b": b
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=str(resultat),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Calcul correct", "points": 2.0}
                ]
            )
        
        elif type_exercice == "poser_operation":
            enonce = f"Poser et calculer : {a} × {b}"
            
            resultat = a * b
            
            # Décomposer b en unités, dizaines, etc.
            str_b = str(b)
            etapes = [
                f"  {a}",
                f"×  {b}",
                "-----"
            ]
            
            # Calcul par ligne
            produits_intermediaires = []
            for i, chiffre in enumerate(reversed(str_b)):
                if chiffre != '0':
                    multiplicateur = int(chiffre) * (10 ** i)
                    produit = a * int(chiffre)
                    if i > 0:
                        etapes.append(f" {produit}{'0' * i}  ({a} × {chiffre} × 10^{i})")
                    else:
                        etapes.append(f"  {produit}  ({a} × {chiffre})")
                    produits_intermediaires.append(produit * (10 ** i))
            
            etapes.append("-----")
            etapes.append(f" {resultat}")
            etapes.append("")
            etapes.append(f"Résultat : {a} × {b} = {resultat}")
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "poser_operation",
                    "enonce": enonce,
                    "a": a,
                    "b": b
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=str(resultat),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Opération posée correctement", "points": 0.5},
                    {"etape": "Produits intermédiaires", "points": 1.0},
                    {"etape": "Résultat final", "points": 0.5}
                ]
            )
        
        else:  # probleme
            # Problèmes contextuels
            themes = [
                {"nom": "objets", "contexte": "achète {b} paquets de {a} bonbons", "question": "Combien de bonbons a-t-elle au total ?"},
                {"nom": "argent", "contexte": "achète {b} articles à {a} € chacun", "question": "Quel est le prix total ?"},
                {"nom": "distance", "contexte": "parcourt {b} fois un circuit de {a} km", "question": "Quelle distance totale a-t-elle parcourue ?"}
            ]
            
            theme = random.choice(themes)
            contexte = theme["contexte"].format(a=a, b=b)
            question = theme["question"]
            
            enonce = f"Marie {contexte}. {question}"
            
            resultat = a * b
            
            if theme["nom"] == "objets":
                unite = "bonbons"
            elif theme["nom"] == "argent":
                unite = "€"
            else:
                unite = "km"
            
            etapes = [
                f"{b} × {a} = {resultat}",
                f"Marie a {resultat} {unite}."
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "probleme",
                    "enonce": enonce,
                    "a": a,
                    "b": b,
                    "theme": theme["nom"]
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=f"{resultat} {unite}",
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Compréhension du problème", "points": 0.5},
                    {"etape": "Opération correcte", "points": 1.0},
                    {"etape": "Résultat avec unité", "points": 0.5}
                ],
                conseils_prof=[
                    "Vérifier que l'élève identifie bien la multiplication",
                    "Insister sur l'importance de l'unité dans la réponse"
                ]
            )


    
    def _gen_division_euclidienne(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur la division euclidienne (6e_N06)
        
        Concepts :
        - Calculer une division (quotient et reste)
        - Poser une division euclidienne
        - Résoudre des problèmes avec division
        """
        
        types_exercices = ["calculer", "poser_operation", "probleme"]
        
        if difficulte == "facile":
            type_exercice = "calculer"
            diviseur = random.randint(2, 10)
            quotient = random.randint(2, 10)
            reste = random.randint(0, diviseur - 1)
            dividende = diviseur * quotient + reste
        elif difficulte == "moyen":
            type_exercice = random.choice(["calculer", "poser_operation"])
            diviseur = random.randint(3, 15)
            quotient = random.randint(5, 20)
            reste = random.randint(0, diviseur - 1)
            dividende = diviseur * quotient + reste
        else:
            type_exercice = random.choice(types_exercices)
            diviseur = random.randint(10, 50)
            quotient = random.randint(10, 50)
            reste = random.randint(0, diviseur - 1)
            dividende = diviseur * quotient + reste
        
        if type_exercice == "calculer":
            enonce = f"Effectuer la division euclidienne de {dividende} par {diviseur}. Donner le quotient et le reste."
            
            etapes = [
                f"{dividende} = {diviseur} × {quotient} + {reste}",
                f"Quotient : {quotient}",
                f"Reste : {reste}",
                f"Vérification : {diviseur} × {quotient} + {reste} = {diviseur * quotient} + {reste} = {dividende}"
            ]
            
            resultat = f"Quotient = {quotient}, Reste = {reste}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer",
                    "enonce": enonce,
                    "dividende": dividende,
                    "diviseur": diviseur
                },
                solution_calculee={"quotient": quotient, "reste": reste, "resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Quotient correct", "points": 1.0},
                    {"etape": "Reste correct", "points": 0.5},
                    {"etape": "Vérification", "points": 0.5}
                ]
            )
        
        elif type_exercice == "poser_operation":
            enonce = f"Poser et effectuer la division euclidienne : {dividende} ÷ {diviseur}"
            
            etapes = [
                f"Division : {dividende} ÷ {diviseur}",
                "",
                "Méthode :",
                f"Combien de fois {diviseur} dans {dividende} ?",
                f"Réponse : {quotient} fois",
                f"{diviseur} × {quotient} = {diviseur * quotient}",
                f"Reste : {dividende} - {diviseur * quotient} = {reste}",
                "",
                f"Résultat : {dividende} = {diviseur} × {quotient} + {reste}",
                f"Quotient = {quotient}, Reste = {reste}"
            ]
            
            resultat = f"Quotient = {quotient}, Reste = {reste}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "poser_operation",
                    "enonce": enonce,
                    "dividende": dividende,
                    "diviseur": diviseur
                },
                solution_calculee={"quotient": quotient, "reste": reste, "resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Opération posée", "points": 0.5},
                    {"etape": "Quotient correct", "points": 1.0},
                    {"etape": "Reste correct", "points": 0.5}
                ]
            )
        
        else:  # probleme
            # Problèmes contextuels avec division
            themes = [
                {"nom": "partage", "contexte": "a {dividende} bonbons et veut les partager équitablement entre {diviseur} amis", "question": "Combien de bonbons chaque ami recevra-t-il ? Combien en restera-t-il ?"},
                {"nom": "rangement", "contexte": "doit ranger {dividende} livres dans des cartons contenant chacun {diviseur} livres", "question": "Combien de cartons complets pourra-t-elle remplir ? Combien de livres resteront ?"},
                {"nom": "transport", "contexte": "doit transporter {dividende} personnes dans des voitures de {diviseur} places", "question": "Combien de voitures pleines faut-il ? Combien de places seront libres dans la dernière voiture ?"}
            ]
            
            theme = random.choice(themes)
            contexte = theme["contexte"].format(dividende=dividende, diviseur=diviseur)
            question = theme["question"]
            
            enonce = f"Marie {contexte}. {question}"
            
            etapes = [
                f"{dividende} ÷ {diviseur} = {quotient} reste {reste}",
                f"Division euclidienne : {dividende} = {diviseur} × {quotient} + {reste}"
            ]
            
            if theme["nom"] == "partage":
                etapes.append(f"Chaque ami recevra {quotient} bonbons et il en restera {reste}.")
                resultat = f"{quotient} bonbons par ami, {reste} restant(s)"
            elif theme["nom"] == "rangement":
                etapes.append(f"Elle pourra remplir {quotient} cartons complets et il restera {reste} livre(s).")
                resultat = f"{quotient} cartons, {reste} livre(s) restant(s)"
            else:
                places_libres = diviseur - reste if reste > 0 else 0
                etapes.append(f"Il faut {quotient + (1 if reste > 0 else 0)} voiture(s). Dans la dernière, il y aura {places_libres} place(s) libre(s).")
                resultat = f"{quotient + (1 if reste > 0 else 0)} voiture(s), {places_libres} place(s) libre(s)"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "probleme",
                    "enonce": enonce,
                    "dividende": dividende,
                    "diviseur": diviseur,
                    "theme": theme["nom"]
                },
                solution_calculee={"quotient": quotient, "reste": reste, "resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Compréhension du problème", "points": 0.5},
                    {"etape": "Division correcte", "points": 1.0},
                    {"etape": "Interprétation du reste", "points": 0.5}
                ],
                conseils_prof=[
                    "Vérifier que l'élève comprend le sens du quotient et du reste",
                    "Insister sur l'interprétation du reste dans le contexte"
                ]
            )


    
    def _gen_multiples_diviseurs(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur multiples et diviseurs, critères de divisibilité (6e_N07)
        
        Concepts :
        - Trouver les multiples d'un nombre
        - Lister les diviseurs d'un nombre
        - Vérifier les critères de divisibilité (2, 3, 4, 5, 9, 10)
        """
        
        types_exercices = ["trouver_multiples", "trouver_diviseurs", "verifier_divisibilite"]
        
        if difficulte == "facile":
            type_exercice = "trouver_multiples"
            nombre = random.randint(2, 10)
        elif difficulte == "moyen":
            type_exercice = "trouver_diviseurs"
            nombre = random.randint(12, 50)
        else:
            type_exercice = "verifier_divisibilite"
            nombre = random.randint(100, 500)
        
        if type_exercice == "trouver_multiples":
            nb_multiples = 5
            enonce = f"Lister les {nb_multiples} premiers multiples de {nombre}."
            
            multiples = [nombre * i for i in range(1, nb_multiples + 1)]
            
            etapes = [
                f"Un multiple de {nombre} est un nombre qui peut s'écrire {nombre} × k (où k est un entier)",
                f"Les {nb_multiples} premiers multiples de {nombre} sont :"
            ]
            
            for i, m in enumerate(multiples, 1):
                etapes.append(f"  {nombre} × {i} = {m}")
            
            resultat = ", ".join(map(str, multiples))
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_multiples",
                    "enonce": enonce,
                    "nombre": nombre
                },
                solution_calculee={"multiples": multiples, "resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Liste complète et correcte", "points": 2.0}
                ]
            )
        
        elif type_exercice == "trouver_diviseurs":
            enonce = f"Lister tous les diviseurs de {nombre}."
            
            # Trouver tous les diviseurs
            diviseurs = []
            for i in range(1, nombre + 1):
                if nombre % i == 0:
                    diviseurs.append(i)
            
            etapes = [
                f"Un diviseur de {nombre} est un nombre qui divise {nombre} sans reste",
                "Cherchons tous les diviseurs :"
            ]
            
            # Montrer quelques divisions
            for d in diviseurs[:min(len(diviseurs), 6)]:
                etapes.append(f"  {nombre} ÷ {d} = {nombre // d} (reste 0) → {d} est un diviseur")
            
            if len(diviseurs) > 6:
                etapes.append(f"  ...")
            
            etapes.append(f"Diviseurs de {nombre} : {', '.join(map(str, diviseurs))}")
            
            # Vérification avec produits
            verification = []
            for i in range(len(diviseurs) // 2 + 1):
                if i < len(diviseurs) // 2 or (len(diviseurs) % 2 == 1 and i == len(diviseurs) // 2):
                    d1 = diviseurs[i]
                    d2 = diviseurs[-(i + 1)]
                    if d1 <= d2:
                        verification.append(f"{nombre} = {d1} × {d2}")
            
            etapes.append("Vérification :")
            etapes.extend(verification[:3])
            
            resultat = ", ".join(map(str, diviseurs))
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_diviseurs",
                    "enonce": enonce,
                    "nombre": nombre
                },
                solution_calculee={"diviseurs": diviseurs, "resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Méthode de recherche", "points": 0.5},
                    {"etape": "Liste complète", "points": 1.5}
                ],
                conseils_prof=[
                    "Vérifier que l'élève cherche systématiquement tous les diviseurs",
                    "Insister sur la méthode : tester tous les nombres de 1 à n"
                ]
            )
        
        else:  # verifier_divisibilite
            # Vérifier les critères de divisibilité
            criteres_a_verifier = random.sample([2, 3, 4, 5, 9, 10], k=3)
            
            enonce = f"Le nombre {nombre} est-il divisible par {', '.join(map(str, criteres_a_verifier))} ? Justifier avec les critères de divisibilité."
            
            etapes = []
            resultats = []
            
            for critere in sorted(criteres_a_verifier):
                if critere == 2:
                    dernier_chiffre = nombre % 10
                    est_divisible = dernier_chiffre % 2 == 0
                    verdict = "est" if est_divisible else "n'est pas"
                    etapes.append(f"Divisibilité par 2 : le dernier chiffre est {dernier_chiffre}, donc {nombre} {verdict} divisible par 2")
                    resultats.append(f"2: {'Oui' if est_divisible else 'Non'}")
                
                elif critere == 3:
                    somme_chiffres = sum(int(c) for c in str(nombre))
                    est_divisible = somme_chiffres % 3 == 0
                    verdict_somme = 'divisible' if est_divisible else 'non divisible'
                    verdict = "est" if est_divisible else "n'est pas"
                    etapes.append(f"Divisibilité par 3 : somme des chiffres = {somme_chiffres}, {verdict_somme} par 3, donc {nombre} {verdict} divisible par 3")
                    resultats.append(f"3: {'Oui' if est_divisible else 'Non'}")
                
                elif critere == 4:
                    deux_derniers = nombre % 100
                    est_divisible = deux_derniers % 4 == 0
                    verdict_deux = 'divisible' if est_divisible else 'non divisible'
                    verdict = "est" if est_divisible else "n'est pas"
                    etapes.append(f"Divisibilité par 4 : les deux derniers chiffres forment {deux_derniers}, {verdict_deux} par 4, donc {nombre} {verdict} divisible par 4")
                    resultats.append(f"4: {'Oui' if est_divisible else 'Non'}")
                
                elif critere == 5:
                    dernier_chiffre = nombre % 10
                    est_divisible = dernier_chiffre in [0, 5]
                    verdict = "est" if est_divisible else "n'est pas"
                    etapes.append(f"Divisibilité par 5 : le dernier chiffre est {dernier_chiffre}, donc {nombre} {verdict} divisible par 5")
                    resultats.append(f"5: {'Oui' if est_divisible else 'Non'}")
                
                elif critere == 9:
                    somme_chiffres = sum(int(c) for c in str(nombre))
                    est_divisible = somme_chiffres % 9 == 0
                    verdict_somme = 'divisible' if est_divisible else 'non divisible'
                    verdict = "est" if est_divisible else "n'est pas"
                    etapes.append(f"Divisibilité par 9 : somme des chiffres = {somme_chiffres}, {verdict_somme} par 9, donc {nombre} {verdict} divisible par 9")
                    resultats.append(f"9: {'Oui' if est_divisible else 'Non'}")
                
                elif critere == 10:
                    dernier_chiffre = nombre % 10
                    est_divisible = dernier_chiffre == 0
                    verdict = "est" if est_divisible else "n'est pas"
                    etapes.append(f"Divisibilité par 10 : le dernier chiffre est {dernier_chiffre}, donc {nombre} {verdict} divisible par 10")
                    resultats.append(f"10: {'Oui' if est_divisible else 'Non'}")
            
            resultat = " | ".join(resultats)
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "verifier_divisibilite",
                    "enonce": enonce,
                    "nombre": nombre,
                    "criteres": criteres_a_verifier
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Application critère 1", "points": 0.7},
                    {"etape": "Application critère 2", "points": 0.7},
                    {"etape": "Application critère 3", "points": 0.6}
                ],
                conseils_prof=[
                    "Vérifier que l'élève connaît les critères de divisibilité",
                    "Insister sur l'application rigoureuse de chaque critère",
                    "Critères à connaître : 2 (dernier chiffre pair), 3 (somme des chiffres divisible par 3), 5 (dernier chiffre 0 ou 5), 9 (somme des chiffres divisible par 9), 10 (dernier chiffre 0)"
                ]
            )


    
    # ============================================================================
    # SPRINT 4 - GÉNÉRATEURS 6e FINAL (N08, N09, GM01, GM02, GM03, SP02)
    # ============================================================================
    
    def _gen_fractions_partage(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur les fractions comme partage et quotient (6e_N08)
        
        Concepts :
        - Partager un objet en parts égales
        - Représenter une fraction
        - Fraction comme quotient de division
        """
        
        types_exercices = ["partager", "representer", "calculer_quotient"]
        
        if difficulte == "facile":
            type_exercice = "partager"
            denominateur = random.choice([2, 3, 4, 5, 6, 8])
            numerateur = random.randint(1, denominateur - 1)
        elif difficulte == "moyen":
            type_exercice = "representer"
            denominateur = random.choice([4, 5, 6, 8, 10, 12])
            numerateur = random.randint(1, denominateur - 1)
        else:
            type_exercice = "calculer_quotient"
            denominateur = random.randint(5, 20)
            numerateur = random.randint(1, denominateur - 1)
        
        if type_exercice == "partager":
            # Partager un objet (gâteau, pizza, etc.)
            objets = ["gâteau", "pizza", "tablette de chocolat", "tarte"]
            objet = random.choice(objets)
            
            enonce = f"Un {objet} est partagé en {denominateur} parts égales. Marie mange {numerateur} part{'s' if numerateur > 1 else ''}. Quelle fraction du {objet} a-t-elle mangée ?"
            
            etapes = [
                f"{numerateur} part{'s' if numerateur > 1 else ''} sur {denominateur} = {numerateur}/{denominateur}",
                f"Marie a mangé {numerateur}/{denominateur} du {objet}."
            ]
            
            resultat = f"{numerateur}/{denominateur}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_FRACTIONS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "partager",
                    "enonce": enonce,
                    "numerateur": numerateur,
                    "denominateur": denominateur,
                    "objet": objet
                },
                solution_calculee={"resultat": resultat, "numerateur": numerateur, "denominateur": denominateur},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Fraction correcte", "points": 2.0}
                ]
            )
        
        elif type_exercice == "representer":
            enonce = f"Représenter la fraction {numerateur}/{denominateur} en coloriant des cases sur une grille de {denominateur} cases."
            
            etapes = [
                f"La fraction {numerateur}/{denominateur} signifie {numerateur} partie(s) sur {denominateur}",
                f"On colorie {numerateur} case(s) sur un total de {denominateur} cases",
                f"Résultat : {numerateur}/{denominateur}"
            ]
            
            resultat = f"{numerateur}/{denominateur} représenté"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_FRACTIONS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "representer",
                    "enonce": enonce,
                    "numerateur": numerateur,
                    "denominateur": denominateur
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Compréhension de la fraction", "points": 1.0},
                    {"etape": "Représentation correcte", "points": 1.0}
                ]
            )
        
        else:  # calculer_quotient
            # Fraction comme quotient
            dividende = numerateur
            diviseur = denominateur
            
            enonce = f"Écrire sous forme de fraction le quotient de la division : {dividende} ÷ {diviseur}"
            
            etapes = [
                f"Un quotient peut s'écrire comme une fraction",
                f"{dividende} ÷ {diviseur} = {dividende}/{diviseur}",
                f"Le dividende {dividende} devient le numérateur",
                f"Le diviseur {diviseur} devient le dénominateur"
            ]
            
            resultat = f"{dividende}/{diviseur}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_FRACTIONS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer_quotient",
                    "enonce": enonce,
                    "dividende": dividende,
                    "diviseur": diviseur
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Écriture en fraction", "points": 2.0}
                ],
                conseils_prof=[
                    "Insister sur le lien entre division et fraction",
                    "Vérifier que l'élève place bien dividende/diviseur"
                ]
            )
    
    def _gen_fractions_simples(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur les fractions simples de l'unité (6e_N09)
        
        Concepts :
        - Lire des fractions simples (1/2, 1/3, 1/4)
        - Comparer des fractions simples
        - Calculer une partie d'un nombre
        """
        
        types_exercices = ["lire_fraction", "comparer", "calculer_partie"]
        
        if difficulte == "facile":
            type_exercice = "lire_fraction"
            fractions_simples = [(1, 2), (1, 3), (1, 4), (1, 5)]
        elif difficulte == "moyen":
            type_exercice = "comparer"
            fractions_simples = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
        else:
            type_exercice = "calculer_partie"
            fractions_simples = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 8)]
        
        if type_exercice == "lire_fraction":
            num, denom = random.choice(fractions_simples)
            
            noms = {2: "demi", 3: "tiers", 4: "quart", 5: "cinquième"}
            nom_fraction = noms.get(denom, f"1/{denom}")
            
            enonce = f"Lire et écrire la fraction suivante : {num}/{denom}"
            
            etapes = [
                f"{num}/{denom} se lit : un {nom_fraction}",
                f"Cela représente 1 partie sur {denom} parties égales"
            ]
            
            resultat = f"un {nom_fraction}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_FRACTIONS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "lire_fraction",
                    "enonce": enonce,
                    "numerateur": num,
                    "denominateur": denom
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Lecture correcte", "points": 2.0}
                ]
            )
        
        elif type_exercice == "comparer":
            frac1 = random.choice(fractions_simples)
            frac2 = random.choice([f for f in fractions_simples if f != frac1])
            
            num1, denom1 = frac1
            num2, denom2 = frac2
            
            enonce = f"Comparer les fractions {num1}/{denom1} et {num2}/{denom2}. Laquelle est la plus grande ?"
            
            # Réduction au même dénominateur (PPCM)
            import math
            ppcm = (denom1 * denom2) // math.gcd(denom1, denom2)
            
            num1_ppcm = num1 * (ppcm // denom1)
            num2_ppcm = num2 * (ppcm // denom2)
            
            etapes = [
                f"Réduction au même dénominateur : {ppcm}",
                f"{num1}/{denom1} = {num1_ppcm}/{ppcm}",
                f"{num2}/{denom2} = {num2_ppcm}/{ppcm}",
            ]
            
            if num1_ppcm > num2_ppcm:
                etapes.append(f"{num1_ppcm}/{ppcm} > {num2_ppcm}/{ppcm}, donc {num1}/{denom1} > {num2}/{denom2}")
                resultat = f"{num1}/{denom1} > {num2}/{denom2}"
            elif num1_ppcm < num2_ppcm:
                etapes.append(f"{num1_ppcm}/{ppcm} < {num2_ppcm}/{ppcm}, donc {num1}/{denom1} < {num2}/{denom2}")
                resultat = f"{num1}/{denom1} < {num2}/{denom2}"
            else:
                etapes.append(f"{num1_ppcm}/{ppcm} = {num2_ppcm}/{ppcm}, donc {num1}/{denom1} = {num2}/{denom2}")
                resultat = f"{num1}/{denom1} = {num2}/{denom2}"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_FRACTIONS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "comparer",
                    "enonce": enonce,
                    "frac1": frac1,
                    "frac2": frac2
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Réduction au même dénominateur", "points": 1.0},
                    {"etape": "Comparaison correcte", "points": 1.0}
                ]
            )
        
        else:  # calculer_partie
            num, denom = random.choice(fractions_simples)
            
            # Choisir un nombre divisible par denom
            multiple = random.randint(3, 20)
            nombre = denom * multiple
            
            enonce = f"Calculer {num}/{denom} de {nombre}."
            
            resultat = (num * nombre) // denom
            
            etapes = [
                f"{num}/{denom} de {nombre} signifie : ({nombre} ÷ {denom}) × {num}",
                f"{nombre} ÷ {denom} = {nombre // denom}",
                f"{nombre // denom} × {num} = {resultat}",
                f"Réponse : {resultat}"
            ]
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_FRACTIONS,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer_partie",
                    "enonce": enonce,
                    "numerateur": num,
                    "denominateur": denom,
                    "nombre": nombre
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=str(resultat),
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Division par le dénominateur", "points": 1.0},
                    {"etape": "Multiplication par le numérateur", "points": 1.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève comprend 'de' = multiplication",
                    "Insister sur l'ordre : diviser puis multiplier"
                ]
            )


    
    def _gen_mesurer_longueurs(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur mesurer et comparer des longueurs (6e_GM01)
        
        Concepts :
        - Mesurer un segment avec règle
        - Comparer deux longueurs
        - Convertir cm ↔ m ↔ km
        """
        
        points = self._get_next_geometry_points()
        
        types_exercices = ["mesurer", "comparer", "convertir"]
        
        if difficulte == "facile":
            type_exercice = "mesurer"
            max_coord = 15
        elif difficulte == "moyen":
            type_exercice = "comparer"
            max_coord = 20
        else:
            type_exercice = "convertir"
            max_coord = 20
        
        if type_exercice == "mesurer":
            # Mesurer un segment
            ax = random.randint(2, 5)
            ay = random.randint(2, 5)
            longueur_cm = random.randint(4, 15)
            bx = ax + longueur_cm
            by = ay
            
            enonce = f"Mesurer la longueur du segment [{points[0]}{points[1]}] sur la figure ci-dessous."
            
            etapes = [
                f"Le segment [{points[0]}{points[1]}] mesure {longueur_cm} cm",
                "Pour mesurer, on utilise une règle graduée en cm"
            ]
            
            resultat = f"{longueur_cm} cm"
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by
            }
            
            figure = GeometricFigure(
                type="segment",
                points=points[:2],
                longueurs_connues=coords,
                proprietes=["with_grid", "segment", "mesure"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "mesurer",
                    "enonce": enonce,
                    "longueur": longueur_cm
                },
                solution_calculee={"resultat": resultat, "longueur": longueur_cm},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Mesure correcte", "points": 2.0}
                ]
            )
        
        elif type_exercice == "comparer":
            # Comparer deux longueurs avec conversions
            longueur1_cm = random.randint(50, 200)
            longueur2_m = round(random.uniform(0.5, 2.0), 1)
            
            enonce = f"Comparer les longueurs : {longueur1_cm} cm et {longueur2_m} m. Laquelle est la plus grande ?"
            
            # Convertir en même unité
            longueur1_m = longueur1_cm / 100
            
            etapes = [
                f"Conversion en mètres :",
                f"{longueur1_cm} cm = {longueur1_cm} ÷ 100 = {longueur1_m} m",
                f"Comparaison : {longueur1_m} m {'<' if longueur1_m < longueur2_m else '>' if longueur1_m > longueur2_m else '='} {longueur2_m} m"
            ]
            
            if longueur1_m < longueur2_m:
                etapes.append(f"Donc {longueur1_cm} cm < {longueur2_m} m")
                resultat = f"{longueur1_cm} cm < {longueur2_m} m"
            elif longueur1_m > longueur2_m:
                etapes.append(f"Donc {longueur1_cm} cm > {longueur2_m} m")
                resultat = f"{longueur1_cm} cm > {longueur2_m} m"
            else:
                etapes.append(f"Donc {longueur1_cm} cm = {longueur2_m} m")
                resultat = f"{longueur1_cm} cm = {longueur2_m} m"
            
            # Schéma simple avec 2 segments
            ax1, ay1 = 2, 3
            bx1 = ax1 + 8
            by1 = ay1
            
            ax2, ay2 = 2, 6
            bx2 = ax2 + 10
            by2 = ay2
            
            coords = {
                f"{points[0]}_x": ax1,
                f"{points[0]}_y": ay1,
                f"{points[1]}_x": bx1,
                f"{points[1]}_y": by1,
                f"{points[2]}_x": ax2,
                f"{points[2]}_y": ay2,
                "D_x": bx2,
                "D_y": by2
            }
            
            figure = GeometricFigure(
                type="segments_comparaison",
                points=points[:3] + ["D"],
                longueurs_connues=coords,
                proprietes=["with_grid", "segments", "comparaison"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "comparer",
                    "enonce": enonce,
                    "longueur1_cm": longueur1_cm,
                    "longueur2_m": longueur2_m
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Conversion correcte", "points": 1.0},
                    {"etape": "Comparaison correcte", "points": 1.0}
                ]
            )
        
        else:  # convertir
            # Conversions cm ↔ m ↔ km
            type_conversion = random.choice(["cm_to_m", "m_to_cm", "m_to_km", "km_to_m"])
            
            if type_conversion == "cm_to_m":
                valeur_cm = random.randint(100, 500)
                enonce = f"Convertir {valeur_cm} cm en mètres."
                valeur_m = valeur_cm / 100
                etapes = [
                    f"1 m = 100 cm",
                    f"{valeur_cm} cm = {valeur_cm} ÷ 100 = {valeur_m} m"
                ]
                resultat = f"{valeur_m} m"
            elif type_conversion == "m_to_cm":
                valeur_m = random.randint(1, 10)
                enonce = f"Convertir {valeur_m} m en centimètres."
                valeur_cm = valeur_m * 100
                etapes = [
                    f"1 m = 100 cm",
                    f"{valeur_m} m = {valeur_m} × 100 = {valeur_cm} cm"
                ]
                resultat = f"{valeur_cm} cm"
            elif type_conversion == "m_to_km":
                valeur_m = random.randint(1000, 5000)
                enonce = f"Convertir {valeur_m} m en kilomètres."
                valeur_km = valeur_m / 1000
                etapes = [
                    f"1 km = 1000 m",
                    f"{valeur_m} m = {valeur_m} ÷ 1000 = {valeur_km} km"
                ]
                resultat = f"{valeur_km} km"
            else:  # km_to_m
                valeur_km = random.randint(1, 10)
                enonce = f"Convertir {valeur_km} km en mètres."
                valeur_m = valeur_km * 1000
                etapes = [
                    f"1 km = 1000 m",
                    f"{valeur_km} km = {valeur_km} × 1000 = {valeur_m} m"
                ]
                resultat = f"{valeur_m} m"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.CALCUL_DECIMAUX,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "convertir",
                    "enonce": enonce,
                    "type_conversion": type_conversion
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Conversion correcte", "points": 2.0}
                ],
                conseils_prof=[
                    "Rappeler les équivalences : 1 m = 100 cm, 1 km = 1000 m",
                    "Vérifier que l'élève multiplie ou divise selon le sens de conversion"
                ]
            )


    
    def _gen_perimetre_figures(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur le périmètre de figures usuelles (6e_GM02)
        
        Concepts :
        - Calculer le périmètre d'un carré, rectangle
        - Trouver un côté manquant
        - Problèmes avec périmètre
        """
        
        points = self._get_next_geometry_points()
        
        types_exercices = ["calculer_perimetre", "trouver_cote", "probleme"]
        
        if difficulte == "facile":
            type_exercice = "calculer_perimetre"
        elif difficulte == "moyen":
            type_exercice = "trouver_cote"
        else:
            type_exercice = "probleme"
        
        if type_exercice == "calculer_perimetre":
            # Calculer périmètre rectangle ou carré
            figure_type = random.choice(["rectangle", "carre"])
            
            if figure_type == "rectangle":
                longueur = random.randint(5, 15)
                largeur = random.randint(3, 10)
                
                enonce = f"Calculer le périmètre d'un rectangle de longueur {longueur} cm et largeur {largeur} cm."
                
                perimetre = 2 * (longueur + largeur)
                
                etapes = [
                    f"Formule du périmètre d'un rectangle : P = 2 × (L + l)",
                    f"P = 2 × ({longueur} + {largeur})",
                    f"P = 2 × {longueur + largeur}",
                    f"P = {perimetre} cm"
                ]
                
                resultat = f"{perimetre} cm"
                
                # Schéma
                ax, ay = 2, 2
                bx, by = ax + longueur, ay
                cx, cy = bx, by + largeur
                dx, dy = ax, cy
            else:  # carre
                cote = random.randint(4, 12)
                
                enonce = f"Calculer le périmètre d'un carré de côté {cote} cm."
                
                perimetre = 4 * cote
                
                etapes = [
                    f"Formule du périmètre d'un carré : P = 4 × c",
                    f"P = 4 × {cote}",
                    f"P = {perimetre} cm"
                ]
                
                resultat = f"{perimetre} cm"
                
                # Schéma
                ax, ay = 2, 2
                bx, by = ax + cote, ay
                cx, cy = bx, by + cote
                dx, dy = ax, cy
                longueur = largeur = cote
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy,
                "D_x": dx,
                "D_y": dy
            }
            
            figure = GeometricFigure(
                type=figure_type,
                points=points[:3] + ["D"],
                longueurs_connues=coords,
                proprietes=["with_grid", figure_type, "perimetre"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer_perimetre",
                    "enonce": enonce,
                    "figure": figure_type,
                    "longueur": longueur,
                    "largeur": largeur
                },
                solution_calculee={"resultat": resultat, "perimetre": perimetre},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Application de la formule", "points": 1.0},
                    {"etape": "Calcul correct", "points": 1.0}
                ]
            )
        
        elif type_exercice == "trouver_cote":
            # Trouver un côté manquant
            perimetre = random.randint(30, 60)
            longueur = random.randint(8, 20)
            
            # P = 2(L + l) donc l = P/2 - L
            largeur = perimetre // 2 - longueur
            
            enonce = f"Un rectangle a un périmètre de {perimetre} cm et une longueur de {longueur} cm. Quelle est sa largeur ?"
            
            etapes = [
                f"Formule : P = 2 × (L + l)",
                f"{perimetre} = 2 × ({longueur} + l)",
                f"{perimetre // 2} = {longueur} + l",
                f"l = {perimetre // 2} - {longueur}",
                f"l = {largeur} cm"
            ]
            
            resultat = f"{largeur} cm"
            
            # Schéma
            ax, ay = 2, 2
            bx, by = ax + min(longueur, 15), ay
            cx, cy = bx, by + min(largeur, 10)
            dx, dy = ax, cy
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy,
                "D_x": dx,
                "D_y": dy
            }
            
            figure = GeometricFigure(
                type="rectangle",
                points=points[:3] + ["D"],
                longueurs_connues=coords,
                proprietes=["with_grid", "rectangle", "perimetre", "trouver_cote"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_cote",
                    "enonce": enonce,
                    "perimetre": perimetre,
                    "longueur": longueur
                },
                solution_calculee={"resultat": resultat, "largeur": largeur},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Utilisation de la formule", "points": 1.0},
                    {"etape": "Résolution correcte", "points": 1.0}
                ]
            )
        
        else:  # probleme
            # Problème avec périmètre
            longueur = random.randint(10, 20)
            largeur = random.randint(5, 15)
            perimetre = 2 * (longueur + largeur)
            
            enonce = f"Marie veut clôturer un jardin rectangulaire de {longueur} m de long et {largeur} m de large. Quelle longueur de clôture doit-elle acheter ?"
            
            etapes = [
                "La longueur de clôture correspond au périmètre du jardin",
                f"P = 2 × (L + l) = 2 × ({longueur} + {largeur})",
                f"P = 2 × {longueur + largeur} = {perimetre} m",
                f"Marie doit acheter {perimetre} m de clôture."
            ]
            
            resultat = f"{perimetre} m"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "probleme",
                    "enonce": enonce,
                    "longueur": longueur,
                    "largeur": largeur
                },
                solution_calculee={"resultat": resultat, "perimetre": perimetre},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Compréhension du problème", "points": 0.5},
                    {"etape": "Calcul du périmètre", "points": 1.5}
                ],
                conseils_prof=[
                    "Vérifier que l'élève identifie bien périmètre = clôture",
                    "Insister sur l'unité (mètres)"
                ]
            )
    
    def _gen_aire_rectangle_carre(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur l'aire du rectangle et du carré (6e_GM03)
        
        Concepts :
        - Calculer l'aire d'un rectangle/carré
        - Trouver un côté à partir de l'aire
        - Problèmes avec aires
        """
        
        points = self._get_next_geometry_points()
        
        types_exercices = ["calculer_aire", "trouver_cote", "probleme"]
        
        if difficulte == "facile":
            type_exercice = "calculer_aire"
        elif difficulte == "moyen":
            type_exercice = "trouver_cote"
        else:
            type_exercice = "probleme"
        
        if type_exercice == "calculer_aire":
            # Calculer aire rectangle ou carré
            figure_type = random.choice(["rectangle", "carre"])
            
            if figure_type == "rectangle":
                longueur = random.randint(4, 10)
                largeur = random.randint(2, 8)
                
                enonce = f"Calculer l'aire d'un rectangle de longueur {longueur} cm et largeur {largeur} cm."
                
                aire = longueur * largeur
                
                etapes = [
                    f"Formule de l'aire d'un rectangle : A = L × l",
                    f"A = {longueur} × {largeur}",
                    f"A = {aire} cm²"
                ]
                
                resultat = f"{aire} cm²"
                
                # Schéma
                ax, ay = 2, 2
                bx, by = ax + longueur, ay
                cx, cy = bx, by + largeur
                dx, dy = ax, cy
            else:  # carre
                cote = random.randint(3, 10)
                
                enonce = f"Calculer l'aire d'un carré de côté {cote} cm."
                
                aire = cote * cote
                
                etapes = [
                    f"Formule de l'aire d'un carré : A = c × c = c²",
                    f"A = {cote} × {cote}",
                    f"A = {aire} cm²"
                ]
                
                resultat = f"{aire} cm²"
                
                # Schéma
                ax, ay = 2, 2
                bx, by = ax + cote, ay
                cx, cy = bx, by + cote
                dx, dy = ax, cy
                longueur = largeur = cote
            
            coords = {
                f"{points[0]}_x": ax,
                f"{points[0]}_y": ay,
                f"{points[1]}_x": bx,
                f"{points[1]}_y": by,
                f"{points[2]}_x": cx,
                f"{points[2]}_y": cy,
                "D_x": dx,
                "D_y": dy
            }
            
            figure = GeometricFigure(
                type=figure_type,
                points=points[:3] + ["D"],
                longueurs_connues=coords,
                proprietes=["with_grid", figure_type, "aire"]
            )
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer_aire",
                    "enonce": enonce,
                    "figure": figure_type,
                    "longueur": longueur,
                    "largeur": largeur
                },
                solution_calculee={"resultat": resultat, "aire": aire},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=figure,
                points_bareme=[
                    {"etape": "Application de la formule", "points": 1.0},
                    {"etape": "Calcul correct", "points": 1.0}
                ]
            )
        
        elif type_exercice == "trouver_cote":
            # Trouver un côté à partir de l'aire
            longueur = random.randint(5, 15)
            largeur = random.randint(3, 12)
            aire = longueur * largeur
            
            enonce = f"Un rectangle a une aire de {aire} cm² et une longueur de {longueur} cm. Quelle est sa largeur ?"
            
            etapes = [
                f"Formule : A = L × l",
                f"{aire} = {longueur} × l",
                f"l = {aire} ÷ {longueur}",
                f"l = {largeur} cm"
            ]
            
            resultat = f"{largeur} cm"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "trouver_cote",
                    "enonce": enonce,
                    "aire": aire,
                    "longueur": longueur
                },
                solution_calculee={"resultat": resultat, "largeur": largeur},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Utilisation de la formule", "points": 1.0},
                    {"etape": "Calcul de la largeur", "points": 1.0}
                ]
            )
        
        else:  # probleme
            # Problème avec aire
            longueur = random.randint(8, 20)
            largeur = random.randint(5, 15)
            aire = longueur * largeur
            
            enonce = f"Marie veut peindre un mur rectangulaire de {longueur} m de long et {largeur} m de haut. Quelle surface doit-elle peindre ?"
            
            etapes = [
                "La surface à peindre correspond à l'aire du mur",
                f"A = L × l = {longueur} × {largeur}",
                f"A = {aire} m²",
                f"Marie doit peindre {aire} m²."
            ]
            
            resultat = f"{aire} m²"
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "probleme",
                    "enonce": enonce,
                    "longueur": longueur,
                    "largeur": largeur
                },
                solution_calculee={"resultat": resultat, "aire": aire},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Compréhension du problème", "points": 0.5},
                    {"etape": "Calcul de l'aire", "points": 1.5}
                ],
                conseils_prof=[
                    "Vérifier que l'élève identifie bien surface = aire",
                    "Insister sur l'unité (m²)"
                ]
            )
    
    def _gen_diagrammes_barres(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """
        Génère un exercice sur les diagrammes en barres et pictogrammes (6e_SP02)
        
        Concepts :
        - Lire une valeur sur un diagramme
        - Comparer deux valeurs
        - Calculer un total
        """
        
        types_exercices = ["lire_diagramme", "comparer", "calculer_total"]
        
        if difficulte == "facile":
            type_exercice = "lire_diagramme"
            nb_categories = 3
            min_val, max_val = 5, 50
        elif difficulte == "moyen":
            type_exercice = "comparer"
            nb_categories = 4
            min_val, max_val = 20, 100
        else:
            type_exercice = "calculer_total"
            nb_categories = 5
            min_val, max_val = 50, 200
        
        # Générer des données
        categories = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin"][:nb_categories]
        valeurs = [random.randint(min_val, max_val) for _ in range(nb_categories)]
        
        if type_exercice == "lire_diagramme":
            categorie_choisie = random.choice(categories)
            index = categories.index(categorie_choisie)
            valeur = valeurs[index]
            
            enonce = f"Sur le diagramme en barres représentant les ventes mensuelles, lire la valeur pour {categorie_choisie}."
            
            etapes = [
                f"Sur le diagramme, la barre de {categorie_choisie} indique {valeur}",
                f"Réponse : {valeur} ventes"
            ]
            
            resultat = f"{valeur} ventes"
            
            # Données pour le diagramme
            data_diagramme = {cat: val for cat, val in zip(categories, valeurs)}
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.STATISTIQUES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "lire_diagramme",
                    "enonce": enonce,
                    "categories": categories,
                    "valeurs": valeurs,
                    "data": data_diagramme,
                    "categorie_choisie": categorie_choisie
                },
                solution_calculee={"resultat": resultat, "valeur": valeur},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Lecture correcte", "points": 2.0}
                ]
            )
        
        elif type_exercice == "comparer":
            # Choisir 2 catégories à comparer
            cat1, cat2 = random.sample(categories, 2)
            val1 = valeurs[categories.index(cat1)]
            val2 = valeurs[categories.index(cat2)]
            
            enonce = f"Sur le diagramme en barres, comparer les ventes de {cat1} ({val1}) et {cat2} ({val2}). Quel mois a eu le plus de ventes ?"
            
            etapes = [
                f"{cat1} : {val1} ventes",
                f"{cat2} : {val2} ventes"
            ]
            
            if val1 > val2:
                etapes.append(f"{val1} > {val2}, donc {cat1} a eu le plus de ventes.")
                resultat = f"{cat1} ({val1} ventes)"
            elif val1 < val2:
                etapes.append(f"{val2} > {val1}, donc {cat2} a eu le plus de ventes.")
                resultat = f"{cat2} ({val2} ventes)"
            else:
                etapes.append(f"{val1} = {val2}, les deux mois ont eu le même nombre de ventes.")
                resultat = f"Égalité ({val1} ventes)"
            
            data_diagramme = {cat: val for cat, val in zip(categories, valeurs)}
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.STATISTIQUES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "comparer",
                    "enonce": enonce,
                    "categories": categories,
                    "valeurs": valeurs,
                    "data": data_diagramme,
                    "cat1": cat1,
                    "cat2": cat2
                },
                solution_calculee={"resultat": resultat},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Lecture des valeurs", "points": 1.0},
                    {"etape": "Comparaison correcte", "points": 1.0}
                ]
            )
        
        else:  # calculer_total
            total = sum(valeurs)
            
            enonce = f"Sur le diagramme en barres représentant les ventes mensuelles de {', '.join(categories)}, calculer le total des ventes."
            
            etapes = [
                f"Ventes : {' + '.join([f'{cat}: {val}' for cat, val in zip(categories, valeurs)])}",
                f"Total = {' + '.join(map(str, valeurs))}",
                f"Total = {total} ventes"
            ]
            
            resultat = f"{total} ventes"
            
            data_diagramme = {cat: val for cat, val in zip(categories, valeurs)}
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.STATISTIQUES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer_total",
                    "enonce": enonce,
                    "categories": categories,
                    "valeurs": valeurs,
                    "data": data_diagramme
                },
                solution_calculee={"resultat": resultat, "total": total},
                etapes_calculees=etapes,
                resultat_final=resultat,
                figure_geometrique=None,
                points_bareme=[
                    {"etape": "Lecture de toutes les valeurs", "points": 1.0},
                    {"etape": "Calcul du total", "points": 1.0}
                ],
                conseils_prof=[
                    "Vérifier que l'élève lit bien toutes les barres",
                    "Insister sur l'addition de toutes les valeurs"
                ]
            )

