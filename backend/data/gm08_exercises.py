"""
GM08 - Exercices figés : Grandeurs et Mesures (Longueurs, Périmètres)
=====================================================================

Chapitre pilote #2 avec 20 exercices validés.
- FREE: ids 1-10
- PREMIUM (PRO): ids 11-20

Ce fichier est la SOURCE UNIQUE pour GM08.
Aucune génération aléatoire - exercices figés et validés.

IMPORTANT: Tout le contenu est en HTML PUR.
- Pas de Markdown (**texte**)
- Pas de LaTeX ($...$)
- Utiliser <strong>, <em>, ×, ÷, etc.

Thèmes couverts:
- Conversions de longueurs (mm, cm, m, km)
- Comparaison de longueurs
- Périmètre de figures simples
- Problèmes concrets (objets, terrains, trajets)
"""

from typing import List, Dict, Any, Optional


# =============================================================================
# 20 EXERCICES GM08 VALIDÉS - HTML PUR (sans Markdown ni LaTeX)
# =============================================================================

GM08_EXERCISES: List[Dict[str, Any]] = [
    # =========================================================================
    # FREE EXERCISES (ids 1-10)
    # =========================================================================
    
    # --- FACILE FREE (4 exercices) ---
    {
        "id": 1,
        "family": "CONVERSION",
        "difficulty": "facile",
        "offer": "free",
        "enonce_html": "<p><strong>Conversion simple (m vers cm) :</strong> Une table mesure <strong>2 mètres</strong> de long. Exprime cette longueur en centimètres.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On veut convertir des mètres en centimètres.</li><li><strong>Méthode :</strong> On sait que 1 m = 100 cm.</li><li><strong>Calculs :</strong> 2 × 100 = 200.</li><li><strong>Conclusion :</strong> La table mesure <strong>200 cm</strong>.</li></ol>",
        "needs_svg": False
    },
    {
        "id": 2,
        "family": "CONVERSION",
        "difficulty": "facile",
        "offer": "free",
        "enonce_html": "<p><strong>Conversion simple (cm vers mm) :</strong> Un crayon mesure <strong>15 centimètres</strong>. Exprime cette longueur en millimètres.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On veut convertir des centimètres en millimètres.</li><li><strong>Méthode :</strong> On sait que 1 cm = 10 mm.</li><li><strong>Calculs :</strong> 15 × 10 = 150.</li><li><strong>Conclusion :</strong> Le crayon mesure <strong>150 mm</strong>.</li></ol>",
        "needs_svg": False
    },
    {
        "id": 3,
        "family": "COMPARAISON",
        "difficulty": "facile",
        "offer": "free",
        "enonce_html": "<p><strong>Comparaison simple :</strong> Marie a un ruban de <strong>50 cm</strong> et Paul a un ruban de <strong>0,5 m</strong>. Qui a le ruban le plus long ?</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On doit comparer deux longueurs exprimées dans des unités différentes.</li><li><strong>Méthode :</strong> Convertir dans la même unité. 0,5 m = 0,5 × 100 = 50 cm.</li><li><strong>Calculs :</strong> Marie : 50 cm, Paul : 50 cm.</li><li><strong>Conclusion :</strong> Les deux rubans ont <strong>la même longueur</strong>.</li></ol>",
        "needs_svg": False
    },
    {
        "id": 4,
        "family": "PERIMETRE",
        "difficulty": "facile",
        "offer": "free",
        "enonce_html": "<p><strong>Périmètre d'un carré :</strong> Un carré a un côté de <strong>5 cm</strong>. Calcule son périmètre.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> Le périmètre est la somme des longueurs des côtés.</li><li><strong>Méthode :</strong> Un carré a 4 côtés égaux. Périmètre = 4 × côté.</li><li><strong>Calculs :</strong> P = 4 × 5 = 20.</li><li><strong>Conclusion :</strong> Le périmètre est de <strong>20 cm</strong>.</li></ol>",
        "needs_svg": False
    },
    
    # --- MOYEN FREE (4 exercices) ---
    {
        "id": 5,
        "family": "CONVERSION",
        "difficulty": "moyen",
        "offer": "free",
        "enonce_html": "<p><strong>Conversion composée (km vers m) :</strong> La distance entre deux villages est de <strong>3,5 kilomètres</strong>. Exprime cette distance en mètres.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On veut convertir des kilomètres en mètres.</li><li><strong>Méthode :</strong> On sait que 1 km = 1000 m.</li><li><strong>Calculs :</strong> 3,5 × 1000 = 3500.</li><li><strong>Conclusion :</strong> La distance est de <strong>3500 m</strong>.</li></ol><p class=\"trap\" style=\"color: orange;\"><strong>Piège classique :</strong> Ne pas oublier de déplacer la virgule de 3 rangs vers la droite.</p>",
        "needs_svg": False
    },
    {
        "id": 6,
        "family": "CONVERSION",
        "difficulty": "moyen",
        "offer": "free",
        "enonce_html": "<p><strong>Conversion inverse (mm vers cm) :</strong> Une vis mesure <strong>35 millimètres</strong>. Exprime cette longueur en centimètres.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On veut convertir des millimètres en centimètres (unité plus grande).</li><li><strong>Méthode :</strong> On divise par 10 car 1 cm = 10 mm.</li><li><strong>Calculs :</strong> 35 ÷ 10 = 3,5.</li><li><strong>Conclusion :</strong> La vis mesure <strong>3,5 cm</strong>.</li></ol>",
        "needs_svg": False
    },
    {
        "id": 7,
        "family": "PERIMETRE",
        "difficulty": "moyen",
        "offer": "free",
        "enonce_html": "<p><strong>Périmètre d'un rectangle :</strong> Un rectangle a une longueur de <strong>8 cm</strong> et une largeur de <strong>5 cm</strong>. Calcule son périmètre.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> Le périmètre d'un rectangle est la somme de tous ses côtés.</li><li><strong>Méthode :</strong> P = 2 × (longueur + largeur) ou P = 2 × L + 2 × l.</li><li><strong>Calculs :</strong> P = 2 × (8 + 5) = 2 × 13 = 26.</li><li><strong>Conclusion :</strong> Le périmètre est de <strong>26 cm</strong>.</li></ol>",
        "needs_svg": False
    },
    {
        "id": 8,
        "family": "COMPARAISON",
        "difficulty": "moyen",
        "offer": "free",
        "enonce_html": "<p><strong>Comparaison avec conversion :</strong> Range dans l'ordre croissant : <strong>2,5 m</strong>, <strong>250 cm</strong>, <strong>2500 mm</strong>, <strong>0,025 km</strong>.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On doit comparer 4 longueurs dans des unités différentes.</li><li><strong>Méthode :</strong> Tout convertir en mètres : 2,5 m = 2,5 m ; 250 cm = 2,5 m ; 2500 mm = 2,5 m ; 0,025 km = 25 m.</li><li><strong>Calculs :</strong> 2,5 m = 2,5 m = 2,5 m < 25 m.</li><li><strong>Conclusion :</strong> Ordre : <strong>2,5 m = 250 cm = 2500 mm < 0,025 km</strong> (les trois premiers sont égaux).</li></ol><p class=\"trap\" style=\"color: orange;\"><strong>Piège classique :</strong> Attention, 0,025 km = 25 m, pas 0,025 m !</p>",
        "needs_svg": False
    },
    
    # --- DIFFICILE FREE (2 exercices) ---
    {
        "id": 9,
        "family": "PROBLEME",
        "difficulty": "difficile",
        "offer": "free",
        "enonce_html": "<p><strong>Problème de trajet :</strong> Lucas fait le tour de son quartier en passant par 4 rues. La première rue mesure <strong>350 m</strong>, la deuxième <strong>0,5 km</strong>, la troisième <strong>425 m</strong> et la quatrième <strong>0,225 km</strong>. Quelle est la distance totale parcourue en mètres ?</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On doit additionner 4 distances exprimées en unités différentes.</li><li><strong>Méthode :</strong> Convertir tout en mètres puis additionner. 0,5 km = 500 m ; 0,225 km = 225 m.</li><li><strong>Calculs :</strong> 350 + 500 + 425 + 225 = 1500.</li><li><strong>Conclusion :</strong> Lucas a parcouru <strong>1500 m</strong> (soit 1,5 km).</li></ol>",
        "needs_svg": False
    },
    {
        "id": 10,
        "family": "PERIMETRE",
        "difficulty": "difficile",
        "offer": "free",
        "enonce_html": "<p><strong>Périmètre complexe :</strong> Un terrain rectangulaire mesure <strong>45 m</strong> de long et <strong>30 m</strong> de large. On veut l'entourer d'une clôture. Quelle longueur de clôture faut-il acheter ? Donne le résultat en mètres puis en kilomètres.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> La clôture fait le tour du terrain, c'est donc le périmètre.</li><li><strong>Méthode :</strong> P = 2 × (L + l) puis convertir en km.</li><li><strong>Calculs :</strong> P = 2 × (45 + 30) = 2 × 75 = 150 m. En km : 150 ÷ 1000 = 0,15 km.</li><li><strong>Conclusion :</strong> Il faut <strong>150 m</strong> de clôture, soit <strong>0,15 km</strong>.</li></ol>",
        "needs_svg": False
    },

    # =========================================================================
    # PREMIUM EXERCISES (ids 11-20)
    # =========================================================================
    
    # --- FACILE PREMIUM (2 exercices) ---
    {
        "id": 11,
        "family": "CONVERSION",
        "difficulty": "facile",
        "offer": "pro",
        "enonce_html": "<p><strong>Conversion rapide (m vers km) :</strong> Un athlète court sur une piste de <strong>400 mètres</strong>. Exprime cette distance en kilomètres.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On veut convertir des mètres en kilomètres (unité plus grande).</li><li><strong>Méthode :</strong> On divise par 1000 car 1 km = 1000 m.</li><li><strong>Calculs :</strong> 400 ÷ 1000 = 0,4.</li><li><strong>Conclusion :</strong> La piste mesure <strong>0,4 km</strong>.</li></ol>",
        "needs_svg": False
    },
    {
        "id": 12,
        "family": "PERIMETRE",
        "difficulty": "facile",
        "offer": "pro",
        "enonce_html": "<p><strong>Périmètre d'un triangle équilatéral :</strong> Un triangle équilatéral a un côté de <strong>7 cm</strong>. Calcule son périmètre.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> Un triangle équilatéral a 3 côtés égaux.</li><li><strong>Méthode :</strong> Périmètre = 3 × côté.</li><li><strong>Calculs :</strong> P = 3 × 7 = 21.</li><li><strong>Conclusion :</strong> Le périmètre est de <strong>21 cm</strong>.</li></ol>",
        "needs_svg": False
    },
    
    # --- MOYEN PREMIUM (3 exercices) ---
    {
        "id": 13,
        "family": "CONVERSION",
        "difficulty": "moyen",
        "offer": "pro",
        "enonce_html": "<p><strong>Double conversion :</strong> Une ficelle mesure <strong>2,75 m</strong>. Exprime cette longueur en millimètres.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On veut passer des mètres aux millimètres.</li><li><strong>Méthode :</strong> On peut passer par les cm ou multiplier directement par 1000. 1 m = 100 cm = 1000 mm.</li><li><strong>Calculs :</strong> 2,75 × 1000 = 2750.</li><li><strong>Conclusion :</strong> La ficelle mesure <strong>2750 mm</strong>.</li></ol>",
        "needs_svg": False
    },
    {
        "id": 14,
        "family": "COMPARAISON",
        "difficulty": "moyen",
        "offer": "pro",
        "enonce_html": "<p><strong>Comparaison de périmètres :</strong> Quel polygone a le plus grand périmètre : un carré de côté <strong>6 cm</strong> ou un rectangle de <strong>7 cm</strong> sur <strong>4 cm</strong> ?</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On doit calculer et comparer deux périmètres.</li><li><strong>Méthode :</strong> P(carré) = 4 × côté ; P(rectangle) = 2 × (L + l).</li><li><strong>Calculs :</strong> P(carré) = 4 × 6 = 24 cm. P(rectangle) = 2 × (7 + 4) = 2 × 11 = 22 cm.</li><li><strong>Conclusion :</strong> Le <strong>carré</strong> a le plus grand périmètre (24 cm > 22 cm).</li></ol>",
        "needs_svg": False
    },
    {
        "id": 15,
        "family": "PROBLEME",
        "difficulty": "moyen",
        "offer": "pro",
        "enonce_html": "<p><strong>Problème de ruban :</strong> Léa veut entourer un cadeau rectangulaire de <strong>30 cm</strong> de long et <strong>20 cm</strong> de large avec un ruban. Elle fait un nœud qui nécessite <strong>25 cm</strong> de ruban en plus. Quelle longueur de ruban lui faut-il ?</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> Le ruban fait le tour du cadeau (périmètre) + longueur pour le nœud.</li><li><strong>Méthode :</strong> P = 2 × (L + l), puis ajouter 25 cm.</li><li><strong>Calculs :</strong> P = 2 × (30 + 20) = 2 × 50 = 100 cm. Total = 100 + 25 = 125 cm.</li><li><strong>Conclusion :</strong> Il faut <strong>125 cm</strong> de ruban (soit 1,25 m).</li></ol>",
        "needs_svg": False
    },
    
    # --- DIFFICILE PREMIUM (5 exercices) ---
    {
        "id": 16,
        "family": "CONVERSION",
        "difficulty": "difficile",
        "offer": "pro",
        "enonce_html": "<p><strong>Conversion avec décimaux :</strong> Convertis <strong>4567 mm</strong> en mètres. Donne le résultat sous forme décimale.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On passe d'une petite unité (mm) à une grande unité (m).</li><li><strong>Méthode :</strong> 1 m = 1000 mm, donc on divise par 1000.</li><li><strong>Calculs :</strong> 4567 ÷ 1000 = 4,567.</li><li><strong>Conclusion :</strong> 4567 mm = <strong>4,567 m</strong>.</li></ol><p class=\"trap\" style=\"color: orange;\"><strong>Piège classique :</strong> Déplacer la virgule de 3 rangs vers la gauche (÷1000), pas vers la droite.</p>",
        "needs_svg": False
    },
    {
        "id": 17,
        "family": "PERIMETRE",
        "difficulty": "difficile",
        "offer": "pro",
        "enonce_html": "<p><strong>Périmètre d'une figure composée :</strong> Une figure est formée d'un carré de côté <strong>4 cm</strong> auquel on a accolé un triangle équilatéral sur l'un de ses côtés. Calcule le périmètre de cette figure.</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> La figure a le périmètre du carré (sans le côté commun) + le périmètre du triangle (sans le côté commun).</li><li><strong>Méthode :</strong> P = 3 côtés du carré + 2 côtés du triangle = 3 × 4 + 2 × 4.</li><li><strong>Calculs :</strong> P = 12 + 8 = 20.</li><li><strong>Conclusion :</strong> Le périmètre est de <strong>20 cm</strong>.</li></ol><p class=\"trap\" style=\"color: orange;\"><strong>Piège classique :</strong> Ne pas compter le côté commun deux fois !</p>",
        "needs_svg": False
    },
    {
        "id": 18,
        "family": "PROBLEME",
        "difficulty": "difficile",
        "offer": "pro",
        "enonce_html": "<p><strong>Problème de course :</strong> Un coureur fait <strong>3 tours</strong> d'un stade rectangulaire de <strong>120 m</strong> de long et <strong>80 m</strong> de large, puis parcourt encore <strong>0,5 km</strong>. Quelle distance totale a-t-il parcourue en mètres ?</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> Distance = 3 × périmètre du stade + 500 m.</li><li><strong>Méthode :</strong> Calculer le périmètre du stade, multiplier par 3, ajouter 500 m.</li><li><strong>Calculs :</strong> P = 2 × (120 + 80) = 400 m. Distance tours = 3 × 400 = 1200 m. Total = 1200 + 500 = 1700 m.</li><li><strong>Conclusion :</strong> Le coureur a parcouru <strong>1700 m</strong> (soit 1,7 km).</li></ol>",
        "needs_svg": False
    },
    {
        "id": 19,
        "family": "COMPARAISON",
        "difficulty": "difficile",
        "offer": "pro",
        "enonce_html": "<p><strong>Comparaison complexe :</strong> Un jardinier a trois parcelles : un carré de <strong>10 m</strong> de côté, un rectangle de <strong>15 m × 6 m</strong>, et un triangle équilatéral de <strong>14 m</strong> de côté. Laquelle nécessite le plus de clôture ?</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> Comparer les périmètres des trois figures.</li><li><strong>Méthode :</strong> P(carré) = 4 × 10 ; P(rectangle) = 2 × (15 + 6) ; P(triangle) = 3 × 14.</li><li><strong>Calculs :</strong> P(carré) = 40 m. P(rectangle) = 42 m. P(triangle) = 42 m.</li><li><strong>Conclusion :</strong> Le <strong>rectangle et le triangle</strong> nécessitent autant de clôture (42 m chacun), plus que le carré (40 m).</li></ol>",
        "needs_svg": False
    },
    {
        "id": 20,
        "family": "PROBLEME",
        "difficulty": "difficile",
        "offer": "pro",
        "enonce_html": "<p><strong>Problème de planification :</strong> Pour un projet d'arts plastiques, Emma doit découper des bandes de papier de <strong>5 cm</strong> de large dans une feuille de <strong>1,2 m</strong> de long. Combien de bandes peut-elle découper ? Quelle longueur de papier restera-t-il ?</p>",
        "solution_html": "<h4>Correction détaillée</h4><ol><li><strong>Compréhension :</strong> On découpe des bandes de 5 cm dans 1,2 m = 120 cm.</li><li><strong>Méthode :</strong> Division euclidienne : 120 ÷ 5 = quotient (nombre de bandes) + reste.</li><li><strong>Calculs :</strong> 120 ÷ 5 = 24 exactement. 24 × 5 = 120, reste = 0.</li><li><strong>Conclusion :</strong> Emma peut découper <strong>24 bandes</strong> et il ne restera <strong>pas de papier</strong>.</li></ol>",
        "needs_svg": False
    }
]


# =============================================================================
# API DE SÉLECTION GM08
# =============================================================================

def get_gm08_exercises(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Retourne les exercices GM08 filtrés par offer et difficulty.
    
    Args:
        offer: "free" ou "pro" (None = "free")
        difficulty: "facile", "moyen", "difficile" (None = tous)
    
    Returns:
        Liste d'exercices filtrés
    """
    # Normaliser l'offre
    offer = (offer or "free").lower()
    
    # Filtrer par offer
    if offer == "pro":
        # Pro voit TOUS les exercices (free + pro)
        filtered = GM08_EXERCISES.copy()
    else:
        # Free ne voit que les exercices free
        filtered = [ex for ex in GM08_EXERCISES if ex["offer"] == "free"]
    
    # Filtrer par difficulté si spécifiée
    if difficulty:
        difficulty = difficulty.lower()
        filtered = [ex for ex in filtered if ex["difficulty"] == difficulty]
    
    return filtered


def get_gm08_batch(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None,
    count: int = 1,
    seed: Optional[int] = None
) -> tuple:
    """
    Retourne un lot d'exercices GM08 SANS DOUBLONS - VERSION PRODUCTION.
    
    Comportement produit:
    - Si pool_size >= count: retourne exactement count exercices UNIQUES
    - Si pool_size < count: retourne pool_size exercices (tous disponibles), avec warning
    - JAMAIS de doublons, JAMAIS d'élargissement de filtre
    
    Args:
        offer: "free" ou "pro"
        difficulty: "facile", "moyen", "difficile"
        count: Nombre d'exercices demandés
        seed: Graine pour le mélange aléatoire (déterministe)
    
    Returns:
        Tuple (exercices: List, metadata: Dict)
        metadata contient:
        - requested: nombre demandé
        - returned: nombre retourné
        - available: nombre disponible après filtrage
        - warning: message si returned < requested (optionnel)
    """
    import random
    
    exercises = get_gm08_exercises(offer=offer, difficulty=difficulty)
    pool_size = len(exercises)
    
    # Cas: aucun exercice disponible
    if not exercises:
        return [], {
            "requested": count,
            "returned": 0,
            "available": 0,
            "warning": f"Aucun exercice disponible pour ce filtre (difficulty={difficulty}, offer={offer})."
        }
    
    # Mélanger avec seed pour reproductibilité
    rng = random.Random(seed) if seed is not None else random.Random()
    shuffled = exercises.copy()
    rng.shuffle(shuffled)
    
    # Déterminer combien d'exercices retourner
    if pool_size >= count:
        # Cas normal: assez d'exercices, prendre les N premiers (tous uniques)
        result = shuffled[:count]
        metadata = {
            "requested": count,
            "returned": count,
            "available": pool_size
        }
    else:
        # Cas insuffisant: retourner tout ce qui est disponible, avec warning
        result = shuffled  # Tous les exercices disponibles
        
        # Construire le message de warning explicite
        filter_desc = []
        if difficulty:
            filter_desc.append(f"difficulté '{difficulty}'")
        if offer and offer != "pro":
            filter_desc.append(f"offre '{offer}'")
        filter_str = " et ".join(filter_desc) if filter_desc else "ce filtre"
        
        metadata = {
            "requested": count,
            "returned": pool_size,
            "available": pool_size,
            "warning": f"Seulement {pool_size} exercice(s) disponible(s) pour {filter_str}."
        }
    
    return result, metadata


def get_exercise_by_seed_index(
    offer: Optional[str] = None,
    difficulty: Optional[str] = None,
    seed: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """
    Retourne un exercice basé sur le seed.
    
    Utilise une combinaison du seed et d'un hash pour sélectionner
    un exercice de manière déterministe mais bien distribuée.
    
    Args:
        offer: "free" ou "pro"
        difficulty: "facile", "moyen", "difficile"
        seed: Graine pour la sélection
    
    Returns:
        Un exercice ou None si aucun ne correspond
    """
    exercises = get_gm08_exercises(offer=offer, difficulty=difficulty)
    
    if not exercises:
        return None
    
    n = len(exercises)
    
    if seed is not None:
        # Hash de Knuth pour bonne distribution
        hash_seed = (seed * 2654435761) % (2**32)
        index = hash_seed % n
    else:
        import random
        index = random.randint(0, n - 1)
    
    return exercises[index]


def get_gm08_stats() -> Dict[str, Any]:
    """Retourne les statistiques des exercices GM08"""
    stats = {
        "total": len(GM08_EXERCISES),
        "by_offer": {"free": 0, "pro": 0},
        "by_difficulty": {"facile": 0, "moyen": 0, "difficile": 0},
        "by_family": {}
    }
    
    for ex in GM08_EXERCISES:
        stats["by_offer"][ex["offer"]] += 1
        stats["by_difficulty"][ex["difficulty"]] += 1
        family = ex["family"]
        stats["by_family"][family] = stats["by_family"].get(family, 0) + 1
    
    return stats
