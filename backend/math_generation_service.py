"""
Service de génération d'exercices mathématiques structurés
Génère specs mathématiques complètes avec solutions calculées (SANS IA)
"""

import random
import math
from fractions import Fraction
from typing import List, Dict, Any, Tuple
import logging
from math_models import (
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
            ["J", "K", "L"],
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
        
        mapping = {
            # 6e
            "Nombres entiers et décimaux": [MathExerciseType.CALCUL_DECIMAUX],
            "Fractions": [MathExerciseType.CALCUL_FRACTIONS],
            "Proportionnalité": [MathExerciseType.PROPORTIONNALITE],
            "Périmètres et aires": [MathExerciseType.PERIMETRE_AIRE, MathExerciseType.RECTANGLE],
            
            # 5e  
            "Triangles": [MathExerciseType.TRIANGLE_QUELCONQUE, MathExerciseType.TRIANGLE_RECTANGLE],
            "Nombres relatifs": [MathExerciseType.CALCUL_RELATIFS],
            "Statistiques": [MathExerciseType.STATISTIQUES],
            
            # 4e
            "Théorème de Pythagore": [MathExerciseType.TRIANGLE_RECTANGLE],
            "Équations": [MathExerciseType.EQUATION_1ER_DEGRE],
            "Puissances": [MathExerciseType.PUISSANCES],
            
            # 3e
            "Probabilités": [MathExerciseType.PROBABILITES],
            "Volumes": [MathExerciseType.VOLUME]
        }
        
        return mapping.get(chapitre, [MathExerciseType.CALCUL_DECIMAUX])
    
    def _generate_spec_by_type(
        self, 
        niveau: str, 
        chapitre: str, 
        exercise_type: MathExerciseType, 
        difficulte: str
    ) -> MathExerciseSpec:
        """Génère une spec selon le type d'exercice"""
        
        generators = {
            MathExerciseType.CALCUL_RELATIFS: self._gen_calcul_relatifs,
            MathExerciseType.CALCUL_FRACTIONS: self._gen_calcul_fractions,
            MathExerciseType.CALCUL_DECIMAUX: self._gen_calcul_decimaux,
            MathExerciseType.EQUATION_1ER_DEGRE: self._gen_equation_1er_degre,
            MathExerciseType.TRIANGLE_RECTANGLE: self._gen_triangle_rectangle,
            MathExerciseType.TRIANGLE_QUELCONQUE: self._gen_triangle_quelconque,
            MathExerciseType.PROPORTIONNALITE: self._gen_proportionnalite,
            MathExerciseType.PERIMETRE_AIRE: self._gen_perimetre_aire,
            MathExerciseType.RECTANGLE: self._gen_rectangle
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
    
    # === GÉNÉRATEURS SPÉCIALISÉS ===
    
    def _gen_triangle_rectangle(
        self, niveau: str, chapitre: str, difficulte: str
    ) -> MathExerciseSpec:
        """Génère un exercice de triangle rectangle (Pythagore)"""
        
        points = self._get_next_geometry_points()
        
        # Générer des longueurs cohérentes
        if difficulte == "facile":
            # Triplets pythagoriciens classiques
            triplets = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
            a, b, c = random.choice(triplets)
        else:
            # Nombres plus complexes
            a = random.randint(6, 15)
            b = random.randint(8, 20) 
            c = math.sqrt(a*a + b*b)
        
        # Choisir quel côté calculer
        angle_droit = points[1]  # B par défaut
        
        if random.choice([True, False]):
            # Donner les deux côtés de l'angle droit, calculer l'hypoténuse
            longueurs_connues = {
                f"{points[0]}{points[1]}": a,
                f"{points[1]}{points[2]}": b
            }
            longueur_a_calculer = f"{points[0]}{points[2]}"
            resultat = c
        else:
            # Donner hypoténuse et un côté, calculer l'autre
            longueurs_connues = {
                f"{points[0]}{points[1]}": a,
                f"{points[0]}{points[2]}": c
            }
            longueur_a_calculer = f"{points[1]}{points[2]}"
            resultat = b
        
        # Créer la figure géométrique
        figure = GeometricFigure(
            type="triangle_rectangle",
            points=points,
            rectangle_en=angle_droit,
            longueurs_connues=longueurs_connues,
            longueurs_a_calculer=[longueur_a_calculer]
        )
        
        # Calculer la solution
        etapes = [
            f"Le triangle {points[0]}{points[1]}{points[2]} est rectangle en {angle_droit}",
            "D'après le théorème de Pythagore :",
        ]
        
        if longueur_a_calculer == f"{points[0]}{points[2]}":
            # Calculer hypoténuse
            etapes.extend([
                f"{longueur_a_calculer}² = {points[0]}{points[1]}² + {points[1]}{points[2]}²",
                f"{longueur_a_calculer}² = {a}² + {b}² = {a*a} + {b*b} = {a*a + b*b}",
                f"{longueur_a_calculer} = √{a*a + b*b} = {resultat:.1f} cm"
            ])
        else:
            # Calculer côté de l'angle droit
            etapes.extend([
                f"{points[0]}{points[2]}² = {points[0]}{points[1]}² + {longueur_a_calculer}²",
                f"{c*c:.0f} = {a}² + {longueur_a_calculer}²",
                f"{longueur_a_calculer}² = {c*c:.0f} - {a*a} = {c*c - a*a:.0f}",
                f"{longueur_a_calculer} = √{c*c - a*a:.0f} = {resultat:.1f} cm"
            ])
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.TRIANGLE_RECTANGLE,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "triangle": f"{points[0]}{points[1]}{points[2]}",
                "angle_droit": angle_droit,
                "longueurs_donnees": longueurs_connues,
                "longueur_a_calculer": longueur_a_calculer
            },
            solution_calculee={
                "longueur_calculee": resultat,
                "unite": "cm",
                "methode": "pythagore"
            },
            etapes_calculees=etapes,
            resultat_final=f"{resultat:.1f} cm",
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
            operations = ["+", "-"]
        else:
            operandes = [random.randint(-20, 20) for _ in range(4)]
            operations = ["+", "-", "*"] if difficulte == "difficile" else ["+", "-"]
        
        # Construire l'expression
        expression = str(operandes[0])
        for i in range(1, len(operandes)):
            op = random.choice(operations)
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
        
        # Calculer le résultat
        resultat = operandes[0]
        for i in range(1, len(operandes)):
            if "+" in expression:
                resultat += operandes[i]
            elif "-" in expression:
                resultat -= operandes[i]
            elif "×" in expression:
                resultat *= operandes[i]
        
        etapes = [
            f"Expression à calculer : {expression}",
            "Calcul étape par étape :",
            f"= {resultat}"
        ]
        
        return MathExerciseSpec(
            niveau=niveau,
            chapitre=chapitre,
            type_exercice=MathExerciseType.CALCUL_RELATIFS,
            difficulte=DifficultyLevel(difficulte),
            parametres={
                "expression": expression,
                "operandes": operandes,
                "operations": operations
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
            f"Tableau de proportionnalité",
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
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
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
                resultat_final=f"Périmètre = {perimetre} cm, Aire = {aire} cm²"
            )
        
        elif figure_type == "carre":
            cote = random.randint(5, 15)
            perimetre = 4 * cote
            aire = cote * cote
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
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
                resultat_final=f"Périmètre = {perimetre} cm, Aire = {aire} cm²"
            )
        
        else:  # cercle
            rayon = random.randint(3, 10)
            perimetre = round(2 * math.pi * rayon, 2)
            aire = round(math.pi * rayon * rayon, 2)
            
            return MathExerciseSpec(
                niveau=niveau,
                chapitre=chapitre,
                type_exercice=MathExerciseType.PERIMETRE_AIRE,
                difficulte=DifficultyLevel(difficulte),
                parametres={
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
                resultat_final=f"Périmètre ≈ {perimetre} cm, Aire ≈ {aire} cm²"
            )
    
    def _gen_rectangle(self, niveau: str, chapitre: str, difficulte: str) -> MathExerciseSpec:
        """Générateur pour rectangles"""
        points = self._get_next_geometry_points()[:4]  # P, Q, R, S par défaut
        
        longueur = random.randint(8, 20)
        largeur = random.randint(4, 12)
        
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