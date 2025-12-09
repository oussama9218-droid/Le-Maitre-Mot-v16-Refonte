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
            "Symétrie centrale": [MathExerciseType.SYMETRIE_CENTRALE],  # ✅ Générateur symétrie centrale ajouté
            
            # ========== 6e - Nombres et calculs (SPRINT 1) ==========
            "Droite numérique et repérage": [MathExerciseType.CALCUL_DECIMAUX],
            
            # ========== 6e - Organisation et gestion de données (SPRINT 1) ==========
            "Lire et compléter des tableaux de données": [MathExerciseType.STATISTIQUES],
            
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
        
        # SPRINT 1 : Générateurs spécifiques par chapitre (priorité sur les types)
        chapter_specific_generators = {
            "Perpendiculaires et parallèles à la règle et à l'équerre": self._gen_perpendiculaires_paralleles,
            "Droite numérique et repérage": self._gen_droite_numerique,
            "Lire et compléter des tableaux de données": self._gen_tableaux_donnees
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
        """Génère un exercice de calculs avec fractions"""
        
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
        else:
            resultat = frac1 - frac2
            expression = f"\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}}"
        
        etapes = [
            f"Expression : {expression}",
            f"Trouver un dénominateur commun : {frac1.denominator * frac2.denominator // math.gcd(frac1.denominator, frac2.denominator)}",
            f"Résultat : \\frac{{{resultat.numerator}}}{{{resultat.denominator}}}"
        ]
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.CALCUL_FRACTIONS,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "fraction1": f"{num1}/{den1}",
                "fraction2": f"{num2}/{den2}",
                "operation": operation,
                "expression": expression
            },
            solution_calculee={
                "resultat_fraction": f"{resultat.numerator}/{resultat.denominator}",
                "resultat_decimal": float(resultat)
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
                "valeurs_donnees": [val1, val2],
                "resultats_donnes": [resultat1, resultat2],
                "valeur_a_trouver": val3,
                "coefficient": k
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
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_AXIALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
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
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_AXIALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
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
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.SYMETRIE_AXIALE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
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
            figure_geometrique=None,
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
            
            etapes = [
                f"Lire la valeur dans le tableau",
                f"Ligne : {nom_ligne}",
                f"Colonne : {nom_colonne}",
                f"Valeur : {valeur}"
            ]
            
            enonce = f"Dans un tableau de {theme['nom']}, quelle est la valeur pour {nom_ligne} dans la colonne {nom_colonne} ?"
            
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
                    "enonce": enonce
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
            
            # Donner un indice : somme de ligne ou colonne
            total_ligne = sum(donnees[ligne])
            total_sans_manquante = total_ligne - valeur_manquante
            
            nom_ligne = theme["lignes"][ligne % len(theme["lignes"])]
            
            etapes = [
                f"Compléter le tableau",
                f"Ligne : {nom_ligne}",
                f"Total de la ligne : {total_ligne}",
                f"Somme des valeurs connues : {total_sans_manquante}",
                f"Valeur manquante = {total_ligne} - {total_sans_manquante} = {valeur_manquante}"
            ]
            
            enonce = f"Dans un tableau de {theme['nom']}, la ligne {nom_ligne} a un total de {total_ligne}. Sachant que la somme des valeurs connues est {total_sans_manquante}, quelle est la valeur manquante ?"
            
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
                    "enonce": enonce
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
            
            if choix == "ligne":
                ligne = random.randint(0, nb_lignes - 1)
                total = sum(donnees[ligne])
                nom = theme["lignes"][ligne % len(theme["lignes"])]
                
                etapes = [
                    f"Calculer le total de la ligne {nom}",
                    f"Valeurs : {' + '.join(map(str, donnees[ligne]))}",
                    f"Total = {total}"
                ]
                
                enonce = f"Dans un tableau de {theme['nom']}, calculer le total de la ligne {nom}. Les valeurs sont : {', '.join(map(str, donnees[ligne]))}."
            else:
                colonne = random.randint(0, nb_colonnes - 1)
                total = sum(donnees[i][colonne] for i in range(nb_lignes))
                nom = theme["colonnes"][colonne % len(theme["colonnes"])]
                
                valeurs_colonne = [donnees[i][colonne] for i in range(nb_lignes)]
                
                etapes = [
                    f"Calculer le total de la colonne {nom}",
                    f"Valeurs : {' + '.join(map(str, valeurs_colonne))}",
                    f"Total = {total}"
                ]
                
                enonce = f"Dans un tableau de {theme['nom']}, calculer le total de la colonne {nom}. Les valeurs sont : {', '.join(map(str, valeurs_colonne))}."
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.STATISTIQUES,
                difficulte=DifficultyLevel(difficulte),
                parametres={
                    "type": "calculer_total",
                    "choix": choix,
                    "nom": nom,
                    "enonce": enonce
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
