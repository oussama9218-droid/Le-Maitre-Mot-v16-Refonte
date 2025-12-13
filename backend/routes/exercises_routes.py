"""
Routes API v1 pour la génération d'exercices
Endpoint: POST /api/v1/exercises/generate

Modes de fonctionnement:
1. Mode legacy: niveau + chapitre (comportement existant)
2. Mode officiel: code_officiel (nouveau, basé sur le référentiel 6e)
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from html import escape
import time
import re

from models.exercise_models import (
    ExerciseGenerateRequest,
    ExerciseGenerateResponse,
    ErrorDetail
)
from models.math_models import MathExerciseType
from services.curriculum_service import curriculum_service
from services.math_generation_service import MathGenerationService
from services.geometry_render_service import GeometryRenderService
from curriculum.loader import get_chapter_by_official_code, CurriculumChapter
from logger import get_logger

logger = get_logger()

router = APIRouter()

# ============================================================================
# INSTANCES GLOBALES DES SERVICES (V1-BE-002-FIX: Performance)
# Instanciation unique pour éviter de recréer les services à chaque requête
# ============================================================================

_math_service = MathGenerationService()
_geom_service = GeometryRenderService()


def generate_exercise_id(niveau: str, chapitre: str) -> str:
    """
    Génère un identifiant unique pour l'exercice
    
    Format: ex_{niveau}_{chapitre_slug}_{timestamp}
    Exemple: ex_5e_symetrie-axiale_1702401234
    
    Args:
        niveau: Niveau scolaire
        chapitre: Nom du chapitre
    
    Returns:
        Identifiant unique
    """
    # Convertir le chapitre en slug (minuscules, tirets)
    chapitre_slug = re.sub(r'[^a-z0-9]+', '-', chapitre.lower()).strip('-')
    
    # Timestamp pour unicité
    timestamp = int(time.time())
    
    return f"ex_{niveau}_{chapitre_slug}_{timestamp}"


def build_enonce_html(enonce: str, svg: Optional[str] = None) -> str:
    """
    Construit l'énoncé HTML à partir de l'énoncé texte et du SVG
    
    NOTE: L'énoncé n'est PAS échappé car il peut contenir du HTML valide
    (tableaux de proportionnalité, etc.) généré par notre code interne.
    
    Args:
        enonce: Énoncé textuel (peut contenir du HTML de tableaux, etc.)
        svg: SVG optionnel (non échappé car généré par notre code interne)
    
    Returns:
        HTML de l'énoncé
    """
    # NOTE: On n'échappe PAS l'énoncé car il peut contenir du HTML valide
    # (tableaux, formules, etc.) généré par notre propre code backend.
    # Ce HTML est de confiance car il provient de math_generation_service.py
    
    html = f"<div class='exercise-enonce'><p>{enonce}</p>"
    
    # Le SVG n'est PAS échappé car il est généré par notre code interne de confiance
    if svg:
        html += f"<div class='exercise-figure'>{svg}</div>"
    
    html += "</div>"
    
    return html


def build_solution_html(etapes: list, resultat_final: str, svg_correction: Optional[str] = None) -> str:
    """
    Construit la solution HTML à partir des étapes et du résultat
    
    NOTE: Les étapes et le résultat ne sont PAS échappés car ils peuvent
    contenir des formules LaTeX ou du HTML généré par notre code interne.
    
    Args:
        etapes: Liste des étapes de résolution (peuvent contenir LaTeX/HTML)
        resultat_final: Résultat final (peut contenir LaTeX/HTML)
        svg_correction: SVG de correction optionnel (non échappé car généré par notre code interne)
    
    Returns:
        HTML de la solution
    """
    html = "<div class='exercise-solution'>"
    html += "<p><strong>Solution :</strong></p>"
    
    if etapes:
        html += "<ol>"
        for etape in etapes:
            # NOTE: On n'échappe PAS les étapes car elles peuvent contenir
            # des formules LaTeX (\\frac{}{}) ou du HTML de confiance
            html += f"<li>{etape}</li>"
        html += "</ol>"
    
    # NOTE: On n'échappe PAS le résultat car il peut contenir du LaTeX
    html += f"<p><strong>Résultat final :</strong> {resultat_final}</p>"
    
    # Le SVG n'est PAS échappé car il est généré par notre code interne de confiance
    if svg_correction:
        html += f"<div class='exercise-figure-correction'>{svg_correction}</div>"
    
    html += "</div>"
    
    return html


def _build_fallback_enonce(spec, chapitre: str) -> str:
    """
    Génère un énoncé pédagogique de fallback basé sur les paramètres de l'exercice
    
    Args:
        spec: Spécification de l'exercice (MathExerciseSpec)
        chapitre: Nom du chapitre
    
    Returns:
        Énoncé lisible pour l'élève
    """
    params = spec.parametres or {}
    
    # 1. Si expression mathématique présente, l'utiliser
    expression = params.get("expression", "")
    if expression:
        return f"Calculer : {expression}"
    
    # 2. Fallback spécifique par type d'exercice
    type_exercice = str(spec.type_exercice).lower() if spec.type_exercice else ""
    
    # Fractions
    if "fractions" in chapitre.lower() or "fraction" in type_exercice:
        frac1 = params.get("fraction1", "")
        frac2 = params.get("fraction2", "")
        operation = params.get("operation", "+")
        if frac1 and frac2:
            op_text = "la somme" if operation == "+" else "la différence"
            return f"Calculer {op_text} des fractions {frac1} et {frac2}. Donner le résultat sous forme de fraction irréductible."
    
    # Équations
    if "equation" in type_exercice or "équation" in chapitre.lower():
        equation = params.get("equation", "")
        if equation:
            return f"Résoudre l'équation suivante : {equation}"
    
    # Calculs décimaux
    if "decimaux" in type_exercice or "décimaux" in chapitre.lower():
        a = params.get("a", "")
        b = params.get("b", "")
        if a and b:
            return f"Effectuer le calcul suivant : {a} et {b}"
    
    # Géométrie - triangles
    if "triangle" in type_exercice or "triangle" in chapitre.lower():
        if params.get("points"):
            return f"Soit le triangle {params.get('points', 'ABC')}. Calculer les mesures demandées."
    
    # Périmètre/Aire
    if "perimetre" in type_exercice or "aire" in type_exercice:
        figure = params.get("figure", params.get("type_figure", "figure"))
        return f"Calculer le périmètre et/ou l'aire de la {figure} donnée."
    
    # Volume - CORRIGÉ P0-001: Toujours inclure les dimensions dans l'énoncé
    if "volume" in type_exercice:
        solide = params.get("solide", params.get("type_solide", "solide"))
        
        # Cube : inclure l'arête
        if solide == "cube":
            arete = params.get("arete", params.get("cote", ""))
            if arete:
                return f"Calculer le volume d'un cube d'arête {arete} cm."
        
        # Pavé droit : inclure les 3 dimensions
        elif solide == "pave" or solide == "pavé" or solide == "pave_droit":
            longueur = params.get("longueur", params.get("L", ""))
            largeur = params.get("largeur", params.get("l", ""))
            hauteur = params.get("hauteur", params.get("h", ""))
            if longueur and largeur and hauteur:
                return f"Calculer le volume d'un pavé droit de dimensions {longueur} cm × {largeur} cm × {hauteur} cm."
        
        # Cylindre : inclure rayon et hauteur
        elif solide == "cylindre":
            rayon = params.get("rayon", params.get("r", ""))
            hauteur = params.get("hauteur", params.get("h", ""))
            if rayon and hauteur:
                return f"Calculer le volume d'un cylindre de rayon {rayon} cm et de hauteur {hauteur} cm."
        
        # Prisme : inclure base et hauteur
        elif solide == "prisme":
            base_longueur = params.get("base_longueur", "")
            base_largeur = params.get("base_largeur", "")
            hauteur = params.get("hauteur", "")
            if base_longueur and base_largeur and hauteur:
                return f"Calculer le volume d'un prisme droit à base rectangulaire de dimensions {base_longueur} cm × {base_largeur} cm et de hauteur {hauteur} cm."
            elif hauteur:
                aire_base = params.get("aire_base", "")
                if aire_base:
                    return f"Calculer le volume d'un prisme d'aire de base {aire_base} cm² et de hauteur {hauteur} cm."
        
        # Fallback avec dimensions si disponibles
        dimensions = []
        for key, label in [("longueur", "L"), ("largeur", "l"), ("hauteur", "h"), 
                           ("arete", "arête"), ("rayon", "r"), ("base_longueur", "base L"),
                           ("base_largeur", "base l")]:
            if key in params and params[key]:
                dimensions.append(f"{label}={params[key]} cm")
        
        if dimensions:
            dims_str = ", ".join(dimensions)
            return f"Calculer le volume du {solide} ({dims_str})."
        
        return f"Calculer le volume du {solide}."
    
    # Probabilités
    if "probabilite" in type_exercice:
        return "Calculer la probabilité demandée."
    
    # Statistiques
    if "statistique" in type_exercice:
        return "Analyser les données statistiques ci-dessous et répondre aux questions."
    
    # 3. Fallback générique amélioré
    # Essayer de construire quelque chose d'utile avec les paramètres disponibles
    if params:
        # Chercher des indices dans les clés des paramètres
        param_keys = list(params.keys())
        if any("nombre" in k.lower() for k in param_keys):
            return f"Effectuer les calculs demandés sur les nombres suivants."
        if any("point" in k.lower() for k in param_keys):
            return "Réaliser la construction géométrique demandée."
    
    # 4. Dernier recours : message générique mais informatif
    return f"Exercice de {chapitre}. Répondre aux questions ci-dessous."


@router.post(
    "/api/v1/exercises/generate",
    response_model=ExerciseGenerateResponse,
    responses={
        422: {
            "model": ErrorDetail,
            "description": "Niveau, chapitre ou code_officiel invalide"
        },
        500: {
            "description": "Erreur lors de la génération de l'exercice"
        }
    },
    summary="Générer un exercice mathématique",
    description="""
    Génère un exercice personnalisé avec énoncé, figure géométrique et solution.
    
    **Deux modes de fonctionnement :**
    
    1. **Mode legacy** : Utiliser `niveau` + `chapitre`
       ```json
       {"niveau": "6e", "chapitre": "Fractions", "difficulte": "moyen"}
       ```
    
    2. **Mode officiel** : Utiliser `code_officiel` (référentiel 6e)
       ```json
       {"code_officiel": "6e_N08", "difficulte": "moyen"}
       ```
    
    Si `code_officiel` est fourni, il a priorité sur `chapitre`.
    """
)
async def generate_exercise(request: ExerciseGenerateRequest):
    """
    Génère un exercice mathématique complet.
    
    Args:
        request: Requête avec niveau/chapitre (legacy) ou code_officiel (nouveau)
    
    Returns:
        Exercice généré avec énoncé HTML, SVG, solution et pdf_token
    """
    
    # ============================================================================
    # 0. RÉSOLUTION DU MODE (code_officiel vs legacy)
    # ============================================================================
    
    curriculum_chapter: Optional[CurriculumChapter] = None
    exercise_types_override: Optional[List[MathExerciseType]] = None
    
    if request.code_officiel:
        # Mode code_officiel : chercher dans le référentiel
        curriculum_chapter = get_chapter_by_official_code(request.code_officiel)
        
        if not curriculum_chapter:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "code_officiel_invalide",
                    "message": f"Le code officiel '{request.code_officiel}' n'existe pas dans le référentiel.",
                    "hint": "Utilisez un code au format 6e_N01, 6e_G01, etc."
                }
            )
        
        # Extraire les informations du référentiel
        request.niveau = curriculum_chapter.niveau
        request.chapitre = curriculum_chapter.chapitre_backend
        
        # Convertir les types d'exercices du référentiel en enum
        if curriculum_chapter.exercise_types:
            try:
                exercise_types_override = [
                    MathExerciseType[et] for et in curriculum_chapter.exercise_types
                    if hasattr(MathExerciseType, et)
                ]
            except Exception as e:
                logger.warning(f"Erreur conversion exercise_types pour {request.code_officiel}: {e}")
        
        logger.info(
            f"Génération exercice (mode officiel): code={request.code_officiel}, "
            f"chapitre_backend={request.chapitre}, exercise_types={curriculum_chapter.exercise_types}"
        )
    else:
        # Mode legacy : utiliser niveau + chapitre directement
        logger.info(
            f"Génération exercice (mode legacy): niveau={request.niveau}, "
            f"chapitre={request.chapitre}, difficulté={request.difficulte}"
        )
    
    # ============================================================================
    # 1. VALIDATION DU NIVEAU
    # ============================================================================
    
    if not curriculum_service.validate_niveau(request.niveau):
        niveaux_disponibles = curriculum_service.get_niveaux_disponibles()
        
        logger.warning(f"Niveau invalide: {request.niveau}")
        
        raise HTTPException(
            status_code=422,
            detail={
                "error": "niveau_invalide",
                "message": (
                    f"Le niveau '{request.niveau}' n'est pas reconnu. "
                    f"Niveaux disponibles : {', '.join(niveaux_disponibles)}."
                ),
                "niveaux_disponibles": niveaux_disponibles
            }
        )
    
    # ============================================================================
    # 2. VALIDATION DU CHAPITRE (sauf si code_officiel a été résolu)
    # ============================================================================
    
    if not curriculum_chapter:
        # Mode legacy : valider le chapitre
        if not curriculum_service.validate_chapitre(request.niveau, request.chapitre):
            chapitres_disponibles = curriculum_service.get_chapitres_disponibles(request.niveau)
            
            logger.warning(
                f"Chapitre invalide: {request.chapitre} pour niveau {request.niveau}"
            )
            
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "chapitre_invalide",
                    "message": (
                        f"Le chapitre '{request.chapitre}' n'existe pas pour le niveau '{request.niveau}'. "
                        f"Chapitres disponibles : {', '.join(chapitres_disponibles[:10])}"
                        + ("..." if len(chapitres_disponibles) > 10 else ".")
                    ),
                    "niveau": request.niveau,
                    "chapitres_disponibles": chapitres_disponibles
                }
            )
    
    # ============================================================================
    # 3. GÉNÉRATION DE L'EXERCICE
    # ============================================================================
    
    try:
        # V1-BE-002-FIX: Utiliser l'instance globale (performance)
        # Générer l'exercice avec le service math
        
        if exercise_types_override and len(exercise_types_override) > 0:
            # Mode code_officiel : utiliser les types spécifiés dans le référentiel
            specs = _math_service.generate_math_exercise_specs_with_types(
                niveau=request.niveau,
                chapitre=request.chapitre,
                difficulte=request.difficulte,
                exercise_types=exercise_types_override,
                nb_exercices=1
            )
        else:
            # Mode legacy : utiliser le mapping par chapitre
            specs = _math_service.generate_math_exercise_specs(
                niveau=request.niveau,
                chapitre=request.chapitre,
                difficulte=request.difficulte,
                nb_exercices=1
            )
        
        if not specs or len(specs) == 0:
            raise ValueError(f"Aucun exercice généré pour {request.niveau} - {request.chapitre}")
        
        spec = specs[0]  # Prendre le premier exercice
        
        logger.info(f"Exercice généré: type={spec.type_exercice}, has_figure={spec.figure_geometrique is not None}")
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération de l'exercice: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération de l'exercice : {str(e)}"
        )
    
    # ============================================================================
    # 4. GÉNÉRATION DU SVG (si figure géométrique présente OU figure_svg dans paramètres)
    # ============================================================================
    
    svg_question = None
    svg_correction = None
    
    # D'abord vérifier si un SVG est directement fourni dans les paramètres
    if spec.parametres and spec.parametres.get("figure_svg"):
        svg_question = spec.parametres.get("figure_svg")
        svg_correction = spec.parametres.get("figure_svg_correction", svg_question)
        logger.info(f"SVG fourni dans paramètres: {len(svg_question or '')} chars")
    
    elif spec.figure_geometrique:
        try:
            # V1-BE-002-FIX: Utiliser l'instance globale (performance)
            result = _geom_service.render_figure_to_svg(spec.figure_geometrique)
            
            # Gérer les deux formats de retour (dict ou string)
            if isinstance(result, dict):
                svg_question = result.get("figure_svg_question", result.get("figure_svg"))
                svg_correction = result.get("figure_svg_correction", result.get("figure_svg"))
            else:
                # Format string simple
                svg_question = result
                svg_correction = result
            
            logger.info(f"SVG généré: question={len(svg_question or '')} chars, correction={len(svg_correction or '')} chars")
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du SVG: {e}", exc_info=True)
            # Continue sans SVG plutôt que de crasher
            svg_question = None
            svg_correction = None
    
    # ============================================================================
    # 5. CONSTRUCTION DE L'ÉNONCÉ ET DE LA SOLUTION HTML
    # ============================================================================
    
    # Énoncé - Priorité : enonce > expression > fallback intelligent
    enonce_text = spec.parametres.get("enonce", "") if spec.parametres else ""
    is_fallback = False
    
    if not enonce_text:
        # Fallback intelligent : générer un énoncé pédagogique à partir des paramètres
        enonce_text = _build_fallback_enonce(spec, request.chapitre)
        is_fallback = True
    
    enonce_html = build_enonce_html(enonce_text, svg_question)
    
    # Solution
    etapes = spec.etapes_calculees or []
    resultat_final = spec.resultat_final or "Solution à compléter"
    solution_html = build_solution_html(etapes, resultat_final, svg_correction)
    
    # ============================================================================
    # 6. GÉNÉRATION DE L'ID ET DU PDF TOKEN
    # ============================================================================
    
    id_exercice = generate_exercise_id(request.niveau, request.chapitre)
    
    # Pour la v1, le pdf_token est simplement l'id_exercice
    # v2: génération de tokens temporaires avec expiration
    pdf_token = id_exercice
    
    # ============================================================================
    # 7. MÉTADONNÉES
    # ============================================================================
    
    # Générer un code de générateur pour debug (ex: "6e_CALCUL_FRACTIONS")
    generator_code = f"{request.niveau}_{spec.type_exercice.name if spec.type_exercice else 'UNKNOWN'}"
    
    metadata = {
        "type_exercice": request.type_exercice,
        "difficulte": request.difficulte,
        "duree_estimee": 5,  # minutes (valeur par défaut)
        "points": 2.0,  # points de barème (valeur par défaut)
        "domaine": curriculum_service.get_domaine_by_chapitre(request.niveau, request.chapitre),
        "has_figure": spec.figure_geometrique is not None or svg_question is not None,
        # Nouveaux champs pour debug/identification du générateur
        "is_fallback": is_fallback,
        "generator_code": generator_code
    }
    
    # ============================================================================
    # 8. CONSTRUCTION DE LA RÉPONSE
    # ============================================================================
    
    response = ExerciseGenerateResponse(
        id_exercice=id_exercice,
        niveau=request.niveau,
        chapitre=request.chapitre,
        enonce_html=enonce_html,
        svg=svg_question,
        solution_html=solution_html,
        pdf_token=pdf_token,
        metadata=metadata
    )
    
    logger.info(f"Exercice généré avec succès: id={id_exercice}")
    
    return response


# Route de santé pour vérifier que le service fonctionne
@router.get(
    "/api/v1/exercises/health",
    summary="Vérifier l'état du service exercises",
    tags=["Health"]
)
async def health_check():
    """Vérifie que le service exercises est opérationnel"""
    
    curriculum_info = curriculum_service.get_curriculum_info()
    
    return {
        "status": "healthy",
        "service": "exercises_v1",
        "curriculum": curriculum_info
    }
