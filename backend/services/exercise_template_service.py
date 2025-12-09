"""
Service de génération d'exercices par TEMPLATE
Système MathALÉA-like avec seed déterministe

Architecture :
- Génération 100% reproductible via seed
- Pas d'appel IA (génération pure template)
- Structure standardisée pour pipeline PDF/IA
"""

import random
import logging
from typing import Dict, List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorClient
import os

from models.mathalea_models import ExerciseType
from models.math_models import MathExerciseSpec, GeometricFigure, MathExerciseType

logger = logging.getLogger(__name__)


class ExerciseTemplateService:
    """
    Service de génération d'exercices par templates
    Reproductible et déterministe via seed
    """
    
    def __init__(self):
        # Connexion MongoDB
        mongo_url = os.environ.get('MONGO_URL')
        if not mongo_url:
            raise ValueError("MONGO_URL environment variable is required")
        
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.mathalea_db  # Use same DB as catalogue and routes
        self.exercise_types_collection = self.db.exercise_types
    
    async def generate_exercise(
        self,
        exercise_type_id: str,
        nb_questions: int,
        seed: int,
        difficulty: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        use_ai_enonce: bool = False,
        use_ai_correction: bool = False
    ) -> Dict[str, Any]:
        """
        Génère un exercice complet à partir d'un ExerciseType
        
        Args:
            exercise_type_id: ID du type d'exercice
            nb_questions: Nombre de questions à générer
            seed: Graine pour reproductibilité
            difficulty: Niveau de difficulté (optionnel)
            options: Options supplémentaires (optionnel)
            use_ai_enonce: Utiliser l'IA pour l'énoncé (non implémenté ici)
            use_ai_correction: Utiliser l'IA pour la correction (non implémenté ici)
        
        Returns:
            Dict contenant l'exercice généré avec ses questions
        
        Raises:
            ValueError: Si l'ExerciseType n'existe pas ou est invalide
        """
        # 1. Charger l'ExerciseType depuis la DB
        exercise_type_dict = await self.exercise_types_collection.find_one(
            {"id": exercise_type_id},
            {"_id": 0}
        )
        
        if not exercise_type_dict:
            raise ValueError(f"ExerciseType with id {exercise_type_id} not found")
        
        exercise_type = ExerciseType(**exercise_type_dict)
        
        # 2. Valider le nombre de questions
        if nb_questions < exercise_type.min_questions:
            raise ValueError(
                f"nb_questions ({nb_questions}) must be >= min_questions ({exercise_type.min_questions})"
            )
        if nb_questions > exercise_type.max_questions:
            raise ValueError(
                f"nb_questions ({nb_questions}) must be <= max_questions ({exercise_type.max_questions})"
            )
        
        # 3. Valider la difficulté
        if difficulty and difficulty not in exercise_type.difficulty_levels:
            raise ValueError(
                f"difficulty '{difficulty}' not in available levels: {exercise_type.difficulty_levels}"
            )
        
        # Utiliser la difficulté par défaut si non spécifiée
        if not difficulty:
            difficulty = exercise_type.difficulty_levels[0] if exercise_type.difficulty_levels else "moyen"
        
        # 4. Initialiser le générateur aléatoire avec la seed
        rng = random.Random(seed)
        
        # 5. Générer les questions selon le type de générateur
        if exercise_type.generator_kind.value == "legacy":
            # Générateur LEGACY (Sprint F.1)
            questions = await self._generate_legacy_questions(
                exercise_type=exercise_type,
                nb_questions=nb_questions,
                difficulty=difficulty,
                seed=seed,
                rng=rng,
                options=options or {}
            )
        else:
            # Générateur TEMPLATE standard
            questions = []
            for i in range(nb_questions):
                question = self._generate_question(
                    exercise_type=exercise_type,
                    question_number=i + 1,
                    difficulty=difficulty,
                    rng=rng,
                    options=options or {}
                )
                questions.append(question)
        
        # 6. Construire la réponse standardisée
        result = {
            "exercise_type_id": exercise_type_id,
            "exercise_type": {
                "code_ref": exercise_type.code_ref,
                "titre": exercise_type.titre,
                "niveau": exercise_type.niveau,
                "domaine": exercise_type.domaine
            },
            "seed": seed,
            "difficulty": difficulty,
            "nb_questions": nb_questions,
            "questions": questions,
            "metadata": {
                "generator_kind": exercise_type.generator_kind.value,
                "supports_seed": exercise_type.supports_seed,
                "competences_ids": exercise_type.competences_ids
            }
        }
        
        logger.info(
            f"✅ Exercice généré: {exercise_type.code_ref}, "
            f"{nb_questions} questions, seed={seed}, difficulty={difficulty}"
        )
        
        return result
    
    def _generate_question(
        self,
        exercise_type: ExerciseType,
        question_number: int,
        difficulty: str,
        rng: random.Random,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Génère une question individuelle
        
        Args:
            exercise_type: Type d'exercice
            question_number: Numéro de la question
            difficulty: Niveau de difficulté
            rng: Générateur aléatoire
            options: Options de génération
        
        Returns:
            Dict contenant la question générée
        """
        # Extraire la configuration aléatoire
        random_config = exercise_type.random_config or {}
        
        # Générer les valeurs selon le type d'exercice
        # Cette logique dépend du contenu de random_config
        data = self._generate_question_data(
            exercise_type=exercise_type,
            difficulty=difficulty,
            random_config=random_config,
            rng=rng,
            options=options
        )
        
        # Générer l'énoncé et la solution
        enonce_brut, solution_brut = self._generate_enonce_and_solution(
            exercise_type=exercise_type,
            data=data,
            difficulty=difficulty
        )
        
        question = {
            "id": f"q{question_number}",
            "enonce_brut": enonce_brut,
            "data": data,
            "solution_brut": solution_brut,
            "metadata": {
                "difficulty": difficulty,
                "competences": exercise_type.competences_ids,
                "question_number": question_number
            }
        }
        
        return question
    
    def _generate_question_data(
        self,
        exercise_type: ExerciseType,
        difficulty: str,
        random_config: Dict[str, Any],
        rng: random.Random,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Génère les données mathématiques de la question
        Selon le type d'exercice et la configuration
        
        Cette fonction est extensible pour supporter différents types d'exercices
        """
        data = {}
        
        # Déterminer les plages de valeurs selon la difficulté
        difficulty_multiplier = {
            "facile": 1.0,
            "moyen": 1.5,
            "difficile": 2.0
        }.get(difficulty, 1.0)
        
        # Extraire les paramètres de random_config
        min_value = random_config.get("min_value", 1)
        max_value = random_config.get("max_value", 10)
        
        # Ajuster selon la difficulté
        adjusted_max = int(max_value * difficulty_multiplier)
        
        # Générer selon le type d'exercice (basé sur question_kinds)
        question_kinds = exercise_type.question_kinds or {}
        
        if question_kinds.get("trouver_valeur"):
            # Type : Trouver une valeur (ex: calcul, géométrie)
            data = self._generate_trouver_valeur_data(
                min_value, adjusted_max, rng, random_config, options
            )
        
        elif question_kinds.get("verifier_propriete"):
            # Type : Vérifier une propriété
            data = self._generate_verifier_propriete_data(
                min_value, adjusted_max, rng, random_config, options
            )
        
        else:
            # Type générique : génération simple
            data = {
                "value_a": rng.randint(min_value, adjusted_max),
                "value_b": rng.randint(min_value, adjusted_max),
                "operation": rng.choice(random_config.get("operations", ["+", "-", "*"]))
            }
        
        return data
    
    def _generate_trouver_valeur_data(
        self,
        min_value: int,
        max_value: int,
        rng: random.Random,
        random_config: Dict[str, Any],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Génère des données pour type 'trouver_valeur'"""
        data = {
            "type": "trouver_valeur",
            "value_a": rng.randint(min_value, max_value),
            "value_b": rng.randint(min_value, max_value)
        }
        
        # Ajouter des paramètres géométriques si spécifié
        if random_config.get("geometry"):
            data["point_a"] = {
                "x": rng.randint(min_value, max_value),
                "y": rng.randint(min_value, max_value)
            }
            data["point_b"] = {
                "x": rng.randint(min_value, max_value),
                "y": rng.randint(min_value, max_value)
            }
        
        return data
    
    def _generate_verifier_propriete_data(
        self,
        min_value: int,
        max_value: int,
        rng: random.Random,
        random_config: Dict[str, Any],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Génère des données pour type 'verifier_propriete'"""
        # Générer une propriété à vérifier (vraie ou fausse)
        is_correct = rng.choice([True, False])
        
        value_a = rng.randint(min_value, max_value)
        
        if is_correct:
            # Générer une valeur qui vérifie la propriété
            value_b = value_a * 2  # Exemple : double
        else:
            # Générer une valeur qui ne vérifie pas la propriété
            value_b = value_a * 2 + rng.randint(1, 3)
        
        data = {
            "type": "verifier_propriete",
            "value_a": value_a,
            "value_b": value_b,
            "expected_answer": is_correct,
            "property_type": random_config.get("property_type", "egalite")
        }
        
        return data
    
    def _generate_enonce_and_solution(
        self,
        exercise_type: ExerciseType,
        data: Dict[str, Any],
        difficulty: str
    ) -> tuple[str, str]:
        """
        Génère l'énoncé et la solution à partir des données
        
        Cette fonction utilise des templates simples
        Pour une vraie implémentation, il faudrait des templates plus sophistiqués
        """
        question_type = data.get("type", "generic")
        
        if question_type == "trouver_valeur":
            enonce = self._generate_enonce_trouver_valeur(data, exercise_type)
            solution = self._generate_solution_trouver_valeur(data, exercise_type)
        
        elif question_type == "verifier_propriete":
            enonce = self._generate_enonce_verifier_propriete(data, exercise_type)
            solution = self._generate_solution_verifier_propriete(data, exercise_type)
        
        else:
            # Template générique
            enonce = (
                f"Question de type {exercise_type.titre}. "
                f"Valeurs : a = {data.get('value_a')}, b = {data.get('value_b')}. "
                f"Opération : {data.get('operation', '+')}."
            )
            
            # Calcul simple
            a = data.get('value_a', 0)
            b = data.get('value_b', 0)
            op = data.get('operation', '+')
            
            if op == '+':
                result = a + b
            elif op == '-':
                result = a - b
            elif op == '*':
                result = a * b
            else:
                result = a
            
            solution = f"Résultat : {result}"
        
        return enonce, solution
    
    def _generate_enonce_trouver_valeur(
        self,
        data: Dict[str, Any],
        exercise_type: ExerciseType
    ) -> str:
        """Génère l'énoncé pour type 'trouver_valeur'"""
        if "point_a" in data and "point_b" in data:
            # Exercice de géométrie
            enonce = (
                f"Soit A({data['point_a']['x']}, {data['point_a']['y']}) "
                f"et B({data['point_b']['x']}, {data['point_b']['y']}). "
                f"Calculer la distance AB."
            )
        else:
            # Exercice numérique
            enonce = (
                f"Calculer : {data['value_a']} + {data['value_b']}"
            )
        
        return enonce
    
    def _generate_solution_trouver_valeur(
        self,
        data: Dict[str, Any],
        exercise_type: ExerciseType
    ) -> str:
        """Génère la solution pour type 'trouver_valeur'"""
        if "point_a" in data and "point_b" in data:
            # Distance euclidienne
            import math
            dx = data['point_b']['x'] - data['point_a']['x']
            dy = data['point_b']['y'] - data['point_a']['y']
            distance = math.sqrt(dx**2 + dy**2)
            
            solution = (
                f"Distance AB = √((x_B - x_A)² + (y_B - y_A)²)\n"
                f"= √(({dx})² + ({dy})²)\n"
                f"= √({dx**2 + dy**2})\n"
                f"≈ {distance:.2f}"
            )
        else:
            # Calcul simple
            result = data['value_a'] + data['value_b']
            solution = f"Résultat : {result}"
        
        return solution
    
    def _generate_enonce_verifier_propriete(
        self,
        data: Dict[str, Any],
        exercise_type: ExerciseType
    ) -> str:
        """Génère l'énoncé pour type 'verifier_propriete'"""
        property_type = data.get("property_type", "egalite")
        
        if property_type == "egalite":
            enonce = (
                f"Vérifier si {data['value_b']} = 2 × {data['value_a']}. "
                f"Répondre par Vrai ou Faux."
            )
        else:
            enonce = (
                f"Vérifier la propriété pour a = {data['value_a']}, b = {data['value_b']}."
            )
        
        return enonce
    
    def _generate_solution_verifier_propriete(
        self,
        data: Dict[str, Any],
        exercise_type: ExerciseType
    ) -> str:
        """Génère la solution pour type 'verifier_propriete'"""
        expected = data.get("expected_answer", False)
        value_a = data['value_a']
        value_b = data['value_b']
        
        solution = (
            f"Calcul : 2 × {value_a} = {2 * value_a}\n"
            f"Comparaison : {value_b} {'=' if expected else '≠'} {2 * value_a}\n"
            f"Réponse : {'Vrai' if expected else 'Faux'}"
        )
        
        return solution

    async def _generate_legacy_questions(
        self,
        exercise_type: ExerciseType,
        nb_questions: int,
        difficulty: str,
        seed: int,
        rng: random.Random,
        options: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Génère des questions en utilisant un générateur legacy
        
        Sprint F.1: Intégration des générateurs legacy dans le système MathALÉA
        
        Args:
            exercise_type: ExerciseType avec generator_kind="legacy"
            nb_questions: Nombre de questions à générer
            difficulty: Niveau de difficulté
            seed: Seed pour reproductibilité
            rng: Générateur aléatoire
            options: Options supplémentaires
        
        Returns:
            Liste de questions au format standardisé
        """
        from services.math_generation_service import MathGenerationService
        from models.math_models import MathExerciseType, MathExerciseSpec
        
        logger.info(
            f"🔄 Génération legacy: {exercise_type.legacy_generator_id}, "
            f"{nb_questions} questions, seed={seed}"
        )
        
        if not exercise_type.legacy_generator_id:
            raise ValueError(
                f"ExerciseType {exercise_type.id} has generator_kind=LEGACY "
                f"but no legacy_generator_id"
            )
        
        # Créer le service legacy
        legacy_service = MathGenerationService()
        
        # Mapper le legacy_generator_id vers MathExerciseType
        try:
            legacy_type = MathExerciseType(exercise_type.legacy_generator_id)
        except ValueError:
            raise ValueError(
                f"Invalid legacy_generator_id: {exercise_type.legacy_generator_id}"
            )
        
        # Les générateurs legacy génèrent généralement 1 question à la fois
        # On appelle le générateur nb_questions fois
        questions = []
        
        for i in range(nb_questions):
            try:
                # Pour l'instant, les générateurs legacy ne sont pas complètement implémentés
                # On génère des questions de fallback professionnelles
                
                # Utiliser une seed unique par question pour variété
                question_seed = seed + i
                question_rng = random.Random(question_seed)
                
                # Générer une question de fallback basée sur le type d'exercice
                question = self._generate_legacy_fallback_question(
                    exercise_type=exercise_type,
                    question_number=i+1,
                    seed=question_seed,
                    difficulty=difficulty,
                    rng=question_rng
                )
                
                questions.append(question)
                
            except Exception as e:
                # Log détaillé côté serveur uniquement
                logger.error(
                    f"Error generating legacy question {i+1} for {exercise_type.code_ref}: {e}",
                    exc_info=True  # Log la stacktrace complète côté serveur
                )
                
                # JAMAIS afficher de stacktrace ou message technique au professeur
                # Option A: On ignore la question et continue
                # Option B: On met une question fallback propre
                
                # Pour l'instant, fallback propre (Option B)
                questions.append({
                    "id": f"q{i+1}",
                    "enonce_brut": "Exercice temporairement indisponible (erreur technique)",
                    "data": {},
                    "solution_brut": "Correction temporairement indisponible",
                    "metadata": {
                        "generator": "legacy",
                        "error_occurred": True,  # Indicateur générique sans détail
                        "fallback": True
                    }
                })
        
        logger.info(f"✅ {len(questions)} questions legacy générées")
        return questions
    
    def _generate_legacy_fallback_question(
        self,
        exercise_type: ExerciseType,
        question_number: int,
        seed: int,
        difficulty: str,
        rng: random.Random
    ) -> Dict[str, Any]:
        """
        Génère une question de fallback pour les exercices legacy
        en attendant l'implémentation complète des générateurs legacy
        
        Cette fonction crée des questions mathématiques réalistes
        basées sur le type d'exercice et le niveau
        """
        legacy_type = exercise_type.legacy_generator_id
        niveau = exercise_type.niveau
        
        # Génération selon le type d'exercice legacy
        # Normaliser le legacy_type pour faciliter la détection
        legacy_type_lower = legacy_type.lower() if legacy_type else ""
        
        if "prop" in legacy_type_lower:
            # Proportionnalité
            a = rng.randint(2, 10)
            b = rng.randint(2, 15)
            c = rng.randint(2, 20)
            d = round((b * c) / a, 2)
            
            enonce = f"Dans un tableau de proportionnalité, on sait que {a} correspond à {b}, et {c} correspond à une valeur inconnue. Quelle est cette valeur ?"
            solution = f"On utilise le produit en croix : (valeur inconnue) × {a} = {b} × {c}\n" \
                      f"valeur inconnue = ({b} × {c}) / {a} = {d}"
        
        elif "sym" in legacy_type_lower and "ax" in legacy_type_lower:
            # Symétrie axiale
            points = ["A", "B", "C", "D", "E", "F"]
            point = rng.choice(points)
            x = rng.randint(-10, 10)
            y = rng.randint(-10, 10)
            
            if seed % 2 == 0:
                # Symétrie par rapport à l'axe des ordonnées
                enonce = f"Le point {point}({x} ; {y}) a pour symétrique {point}' par rapport à l'axe des ordonnées. Quelles sont les coordonnées de {point}' ?"
                solution = f"Par symétrie axiale par rapport à l'axe des ordonnées (droite d'équation x = 0), l'abscisse change de signe et l'ordonnée reste identique.\n" \
                          f"Les coordonnées de {point}' sont ({-x} ; {y})."
            else:
                # Symétrie par rapport à l'axe des abscisses
                enonce = f"Le point {point}({x} ; {y}) a pour symétrique {point}' par rapport à l'axe des abscisses. Quelles sont les coordonnées de {point}' ?"
                solution = f"Par symétrie axiale par rapport à l'axe des abscisses (droite d'équation y = 0), l'abscisse reste identique et l'ordonnée change de signe.\n" \
                          f"Les coordonnées de {point}' sont ({x} ; {-y})."
        
        elif "pourc" in legacy_type_lower:
            # Pourcentages
            total = rng.randint(100, 1000)
            percent = rng.choice([10, 15, 20, 25, 30, 40, 50, 75])
            result = round((total * percent) / 100, 2)
            
            enonce = f"Calculer {percent}% de {total}."
            solution = f"Pour calculer {percent}% de {total}, on effectue : ({percent} × {total}) / 100 = {result}"
        
        elif "calc" in legacy_type_lower and "dec" in legacy_type_lower:
            # Calculs avec décimaux
            a = round(rng.uniform(1, 50), 1)
            b = round(rng.uniform(1, 30), 1)
            operation = rng.choice(["+", "-", "×"])
            
            if operation == "+":
                result = round(a + b, 2)
                enonce = f"Calculer : {a} + {b}"
                solution = f"{a} + {b} = {result}"
            elif operation == "-":
                result = round(a - b, 2)
                enonce = f"Calculer : {a} - {b}"
                solution = f"{a} - {b} = {result}"
            else:  # multiplication
                result = round(a * b, 2)
                enonce = f"Calculer : {a} × {b}"
                solution = f"{a} × {b} = {result}"
        
        else:
            # Type inconnu ou générique - fournir une question générique mais professionnelle
            enonce = f"Question d'exercice de géométrie ou de calcul (niveau {niveau})"
            solution = f"La correction de cet exercice est en cours de développement."
        
        return {
            "id": f"q{question_number}",
            "enonce_brut": enonce,
            "data": {
                "seed": seed,
                "difficulty": difficulty
            },
            "solution_brut": solution,
            "metadata": {
                "generator": "legacy_fallback",
                "legacy_type": legacy_type,
                "seed": seed,
                "difficulty": difficulty,
                "note": "Question générée par fallback en attendant implémentation complète"
            }
        }


# Instance globale
exercise_template_service = ExerciseTemplateService()

# Export
__all__ = [
    "ExerciseTemplateService",
    "exercise_template_service"
]
