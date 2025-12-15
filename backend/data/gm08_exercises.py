"""
GM08 - Exercices figés : Grandeurs et Mesures (Longueurs, Périmètres)
=========================================================================

Chapitre pilote avec 0 exercices validés.
- FREE: ids 1-10
- PREMIUM (PRO): ids 11-20

Ce fichier est la SOURCE UNIQUE pour GM08.
Aucune génération aléatoire - exercices figés et validés.

IMPORTANT: Tout le contenu est en HTML PUR.
- Pas de Markdown (**texte**)
- Pas de LaTeX ($...$)
- Utiliser <strong>, <em>, ×, ÷, etc.

⚠️ FICHIER GÉNÉRÉ AUTOMATIQUEMENT PAR L'ADMIN
   Ne pas modifier manuellement - utiliser /admin/curriculum
"""

from typing import List, Dict, Any, Optional
import random


# =============================================================================
# 0 EXERCICES GM08 VALIDÉS - HTML PUR (sans Markdown ni LaTeX)
# =============================================================================

GM08_EXERCISES: List[Dict[str, Any]] = [
]


# =============================================================================
# FONCTIONS D'ACCÈS AUX EXERCICES (Compatible avec handlers)
# =============================================================================


def get_gm08_exercises(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filtre les exercices selon les critères.
    
    Args:
        offer: "free" ou "pro" (None = tous selon règles)
        difficulty: "facile", "moyen", "difficile" (None = tous)
    
    Returns:
        Liste d'exercices filtrés
    """
    exercises = GM08_EXERCISES
    
    # Filtrer par offer
    if offer:
        offer = offer.lower()
        if offer == "free":
            exercises = [ex for ex in exercises if ex["offer"] == "free"]
        elif offer == "pro":
            pass  # PRO voit tout
    else:
        # Par défaut, FREE ne voit que free
        exercises = [ex for ex in exercises if ex["offer"] == "free"]
    
    # Filtrer par difficulté
    if difficulty:
        difficulty = difficulty.lower()
        exercises = [ex for ex in exercises if ex["difficulty"] == difficulty]
    
    return exercises


def get_random_gm08_exercise(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None,
    seed: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """
    Sélectionne UN exercice aléatoire.
    
    Args:
        offer: "free" ou "pro" (None = free par défaut)
        difficulty: "facile", "moyen", "difficile" (None = tous)
        seed: graine pour reproductibilité (optionnel)
    
    Returns:
        Un exercice aléatoire ou None si aucun disponible
    """
    available = get_gm08_exercises(offer=offer, difficulty=difficulty)
    
    if not available:
        return None
    
    if seed is not None:
        random.seed(seed)
    
    return random.choice(available)


def get_gm08_batch(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None,
    count: int = 1,
    seed: Optional[int] = None
) -> tuple:
    """
    Génère un batch d'exercices SANS DOUBLONS.
    
    Args:
        offer: "free" ou "pro"
        difficulty: filtre optionnel
        count: nombre d'exercices demandés
        seed: graine pour reproductibilité
    
    Returns:
        Tuple (exercices: List, batch_metadata: Dict)
    """
    available = get_gm08_exercises(offer=offer, difficulty=difficulty)
    pool_size = len(available)
    
    batch_meta = {
        "requested": count,
        "available": pool_size,
        "returned": 0,
        "filters": {
            "offer": offer or "free",
            "difficulty": difficulty
        }
    }
    
    if pool_size == 0:
        batch_meta["warning"] = f"Aucun exercice disponible pour les filtres sélectionnés."
        return [], batch_meta
    
    # Mélanger avec seed pour reproductibilité
    if seed is not None:
        random.seed(seed)
    
    shuffled = available.copy()
    random.shuffle(shuffled)
    
    # Prendre au maximum ce qui est disponible
    actual_count = min(count, pool_size)
    selected = shuffled[:actual_count]
    
    batch_meta["returned"] = actual_count
    
    if actual_count < count:
        batch_meta["warning"] = f"Seulement {pool_size} exercices disponibles pour les filtres sélectionnés ({count} demandés)."
    
    return selected, batch_meta


def get_exercise_by_seed_index(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None,
    seed: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """
    Sélectionne UN exercice de manière déterministe.
    """
    available = get_gm08_exercises(offer=offer, difficulty=difficulty)
    
    if not available:
        return None
    
    if seed is not None:
        random.seed(seed)
        index = random.randint(0, len(available) - 1)
    else:
        index = random.randint(0, len(available) - 1)
    
    return available[index]


def get_gm08_stats() -> Dict[str, Any]:
    """Statistiques sur les exercices"""
    exercises = GM08_EXERCISES
    
    stats = {
        "total": len(exercises),
        "by_offer": {"free": 0, "pro": 0},
        "by_difficulty": {"facile": 0, "moyen": 0, "difficile": 0},
        "by_family": {}
    }
    
    for ex in exercises:
        stats["by_offer"][ex["offer"]] = stats["by_offer"].get(ex["offer"], 0) + 1
        stats["by_difficulty"][ex["difficulty"]] = stats["by_difficulty"].get(ex["difficulty"], 0) + 1
        
        family = ex["family"]
        stats["by_family"][family] = stats["by_family"].get(family, 0) + 1
    
    return stats
