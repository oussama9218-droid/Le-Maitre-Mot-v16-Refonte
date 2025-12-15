"""
GM07 Handler - Gestionnaire dédié pour le chapitre pilote
=========================================================

Ce handler intercepte les requêtes pour code_officiel="6e_GM07"
et retourne des exercices depuis la source figée (gm07_exercises.py).

Logique métier:
- FREE: ne voit que les exercices offer="free" (ids 1-10)
- PRO: voit tous les exercices (ids 1-20)
- La difficulté filtre réellement les exercices disponibles
- Génération de lots SANS DOUBLONS (tant que possible)
"""

import random
import time
from typing import Dict, Any, Optional, List
from data.gm07_exercises import (
    get_random_gm07_exercise, 
    get_gm07_exercises, 
    get_gm07_stats,
    get_gm07_batch,
    get_exercise_by_seed_index
)
from services.svg_render_service import render_clock_for_exercise


def is_gm07_request(code_officiel: Optional[str]) -> bool:
    """
    Vérifie si la requête concerne le chapitre GM07.
    
    Args:
        code_officiel: Le code officiel du chapitre
    
    Returns:
        True si c'est une requête GM07
    """
    return code_officiel and code_officiel.upper() == "6E_GM07"


def _format_exercise_response(exercise: Dict[str, Any], timestamp: int) -> Dict[str, Any]:
    """
    Formate un exercice brut en réponse API.
    
    Args:
        exercise: Exercice brut depuis gm07_exercises.py
        timestamp: Timestamp pour l'ID unique
    
    Returns:
        Exercice formaté pour l'API
    """
    is_premium = exercise["offer"] == "pro"
    exercise_id = f"ex_6e_gm07_{exercise['id']}_{timestamp}"
    
    # Générer le SVG si nécessaire
    figure_svg = render_clock_for_exercise(exercise) if exercise.get("needs_svg") else None
    
    return {
        "id_exercice": exercise_id,
        "niveau": "6e",
        "chapitre": "Durées et lecture de l'heure",
        "enonce_html": exercise["enonce_html"],
        "solution_html": exercise["solution_html"],
        "figure_svg": figure_svg,
        "svg": figure_svg,  # Compatibilité avec l'ancien champ
        "pdf_token": exercise_id,
        "metadata": {
            "code_officiel": "6e_GM07",
            "difficulte": exercise["difficulty"],
            "difficulty": exercise["difficulty"],
            "is_premium": is_premium,
            "offer": "pro" if is_premium else "free",
            "generator_code": f"6e_GM07_{exercise['family']}",
            "family": exercise["family"],
            "exercise_id": exercise["id"],
            "is_fallback": False,
            "source": "gm07_fixed_exercises",
            "needs_svg": exercise.get("needs_svg", False)
        }
    }


def generate_gm07_exercise(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None,
    seed: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """
    Génère UN exercice GM07 depuis la source figée.
    
    Utilise le seed pour sélectionner un index déterministe,
    garantissant que des seeds différents retournent des exercices différents.
    
    Args:
        offer: "free" ou "pro" (défaut: "free")
        difficulty: "facile", "moyen", "difficile" (défaut: tous)
        seed: Graine pour la sélection (utilisée comme index déterministe)
    
    Returns:
        Exercice formaté pour l'API ou None si aucun exercice disponible
    """
    # Normaliser les paramètres
    offer = (offer or "free").lower()
    if difficulty:
        difficulty = difficulty.lower()
    
    # Sélectionner un exercice basé sur le seed (sélection déterministe)
    exercise = get_exercise_by_seed_index(
        offer=offer,
        difficulty=difficulty,
        seed=seed
    )
    
    if not exercise:
        return None
    
    timestamp = int(time.time() * 1000)
    return _format_exercise_response(exercise, timestamp)


def generate_gm07_batch(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None,
    count: int = 1,
    seed: Optional[int] = None
) -> tuple:
    """
    Génère un LOT d'exercices GM07 SANS DOUBLONS - VERSION PRODUCTION.
    
    Comportement produit:
    - Si pool_size >= count: retourne exactement count exercices UNIQUES
    - Si pool_size < count: retourne pool_size exercices avec metadata.warning
    - JAMAIS de doublons
    
    Args:
        offer: "free" ou "pro" (défaut: "free")
        difficulty: "facile", "moyen", "difficile" (défaut: tous)
        count: Nombre d'exercices demandés
        seed: Graine pour le mélange aléatoire
    
    Returns:
        Tuple (exercices: List[Dict], batch_metadata: Dict)
        - exercices: Liste d'exercices formatés pour l'API
        - batch_metadata: Infos sur le batch (requested, returned, available, warning?)
    """
    # Normaliser les paramètres
    offer = (offer or "free").lower()
    if difficulty:
        difficulty = difficulty.lower()
    
    # Obtenir le lot sans doublons
    exercises, batch_meta = get_gm07_batch(
        offer=offer,
        difficulty=difficulty,
        count=count,
        seed=seed
    )
    
    if not exercises:
        return [], batch_meta
    
    # Formater chaque exercice avec un timestamp unique
    base_timestamp = int(time.time() * 1000)
    result = []
    
    for idx, exercise in enumerate(exercises):
        formatted = _format_exercise_response(exercise, base_timestamp + idx)
        
        # Ajouter les métadonnées de batch à chaque exercice
        formatted["metadata"]["batch_info"] = {
            "position": idx + 1,
            "total_in_batch": len(exercises),
            "requested": batch_meta["requested"],
            "available": batch_meta["available"]
        }
        
        # Ajouter le warning si présent (uniquement sur le premier exercice)
        if idx == 0 and "warning" in batch_meta:
            formatted["metadata"]["warning"] = batch_meta["warning"]
        
        result.append(formatted)
    
    return result, batch_meta


def get_gm07_available_exercises(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retourne les informations sur les exercices GM07 disponibles.
    Utile pour le debug et les tests.
    """
    exercises = get_gm07_exercises(offer=offer, difficulty=difficulty)
    
    return {
        "count": len(exercises),
        "exercises": [
            {
                "id": ex["id"],
                "family": ex["family"],
                "difficulty": ex["difficulty"],
                "offer": ex["offer"]
            }
            for ex in exercises
        ],
        "filters_applied": {
            "offer": offer or "free",
            "difficulty": difficulty or "all"
        }
    }


def _generate_clock_svg() -> str:
    """
    Génère un SVG d'horloge vide pour les exercices qui en ont besoin.
    L'horloge est vide car l'exercice demande de lire/positionner les aiguilles.
    """
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Cadran -->
  <circle cx="100" cy="100" r="95" fill="#fff" stroke="#333" stroke-width="3"/>
  
  <!-- Centre -->
  <circle cx="100" cy="100" r="4" fill="#333"/>
  
  <!-- Graduations des heures -->
  <g stroke="#333" stroke-width="2">
    <!-- 12h --><line x1="100" y1="15" x2="100" y2="25"/>
    <!-- 1h --><line x1="142.5" y1="22.5" x2="137.5" y2="31"/>
    <!-- 2h --><line x1="177.5" y1="57.5" x2="169" y2="62.5"/>
    <!-- 3h --><line x1="185" y1="100" x2="175" y2="100"/>
    <!-- 4h --><line x1="177.5" y1="142.5" x2="169" y2="137.5"/>
    <!-- 5h --><line x1="142.5" y1="177.5" x2="137.5" y2="169"/>
    <!-- 6h --><line x1="100" y1="185" x2="100" y2="175"/>
    <!-- 7h --><line x1="57.5" y1="177.5" x2="62.5" y2="169"/>
    <!-- 8h --><line x1="22.5" y1="142.5" x2="31" y2="137.5"/>
    <!-- 9h --><line x1="15" y1="100" x2="25" y2="100"/>
    <!-- 10h --><line x1="22.5" y1="57.5" x2="31" y2="62.5"/>
    <!-- 11h --><line x1="57.5" y1="22.5" x2="62.5" y2="31"/>
  </g>
  
  <!-- Chiffres -->
  <g font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">
    <text x="100" y="40">12</text>
    <text x="150" y="55">1</text>
    <text x="170" y="90">2</text>
    <text x="170" y="108">3</text>
    <text x="170" y="125">4</text>
    <text x="150" y="160">5</text>
    <text x="100" y="175">6</text>
    <text x="50" y="160">7</text>
    <text x="30" y="125">8</text>
    <text x="30" y="108">9</text>
    <text x="30" y="90">10</text>
    <text x="50" y="55">11</text>
  </g>
  
  <!-- Note: Aiguilles à positionner mentalement par l'élève -->
  <text x="100" y="130" font-family="Arial" font-size="10" text-anchor="middle" fill="#666">
    (Horloge de référence)
  </text>
</svg>'''


# =============================================================================
# STATISTIQUES GM07 (pour debug)
# =============================================================================

def get_gm07_chapter_info() -> Dict[str, Any]:
    """Retourne les informations complètes sur le chapitre GM07"""
    stats = get_gm07_stats()
    
    return {
        "code_officiel": "6e_GM07",
        "titre": "Durées et lecture de l'heure",
        "niveau": "6e",
        "domaine": "Grandeurs et mesures",
        "type": "chapitre_pilote",
        "source": "exercices_figes",
        "statistics": stats,
        "rules": {
            "free_range": "ids 1-10",
            "pro_range": "ids 11-20",
            "difficulty_levels": ["facile", "moyen", "difficile"],
            "families": ["LECTURE_HORLOGE", "CONVERSION", "CALCUL_DUREE", "PROBLEME_DUREES"]
        }
    }
