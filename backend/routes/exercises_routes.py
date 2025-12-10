"""
Routes API v1 pour la génération d'exercices
Endpoint: POST /api/v1/exercises/generate
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from html import escape
import time
import re

from models.exercise_models import (
    ExerciseGenerateRequest,
    ExerciseGenerateResponse,
    ErrorDetail
)
from services.curriculum_service import curriculum_service
from services.math_generation_service import MathGenerationService
from services.geometry_render_service import GeometryRenderService
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
    
    V1-BE-002-FIX: Échappement HTML pour prévenir les injections XSS
    
    Args:
        etapes: Liste des étapes de résolution (seront échappées)
        resultat_final: Résultat final (sera échappé)
        svg_correction: SVG de correction optionnel (non échappé car généré par notre code interne)
    
    Returns:
        HTML de la solution
    """
    html = "<div class='exercise-solution'>"
    html += "<p><strong>Solution :</strong></p>"
    
    if etapes:
        html += "<ol>"
        for etape in etapes:
            # Échapper chaque étape pour prévenir les injections XSS
            etape_escaped = escape(str(etape))
            html += f"<li>{etape_escaped}</li>"
        html += "</ol>"
    
    # Échapper le résultat final
    resultat_escaped = escape(str(resultat_final))
    html += f"<p><strong>Résultat final :</strong> {resultat_escaped}</p>"
    
    # Le SVG n'est PAS échappé car il est généré par notre code interne de confiance
    if svg_correction:
        html += f"<div class='exercise-figure-correction'>{svg_correction}</div>"
    
    html += "</div>"
    
    return html


@router.post(
    "/api/v1/exercises/generate",
    response_model=ExerciseGenerateResponse,
    responses={
        422: {
            "model": ErrorDetail,
            "description": "Niveau ou chapitre invalide"
        },
        500: {
            "description": "Erreur lors de la génération de l'exercice"
        }
    },
    summary="Générer un exercice mathématique",
    description="Génère un exercice personnalisé avec énoncé, figure géométrique et solution"
)
async def generate_exercise(request: ExerciseGenerateRequest):
    """
    Génère un exercice mathématique complet
    
    - **niveau**: Niveau scolaire (CP, CE1, 6e, 5e, etc.)
    - **chapitre**: Chapitre du curriculum
    - **type_exercice**: Type d'exercice (standard par défaut)
    - **difficulte**: Niveau de difficulté (facile, moyen, difficile)
    
    Returns:
        Exercice généré avec énoncé HTML, SVG, solution et pdf_token
    """
    logger.info(
        f"Génération exercice: niveau={request.niveau}, "
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
    # 2. VALIDATION DU CHAPITRE
    # ============================================================================
    
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
        # Générer l'exercice avec le service math (génère 1 exercice)
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
    # 4. GÉNÉRATION DU SVG (si figure géométrique présente)
    # ============================================================================
    
    svg_question = None
    svg_correction = None
    
    if spec.figure_geometrique:
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
    
    # Énoncé
    enonce_text = spec.parametres.get("enonce", "") if spec.parametres else ""
    if not enonce_text:
        # Fallback sur l'énoncé générique
        enonce_text = f"Exercice de {request.chapitre}"
    
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
    
    metadata = {
        "type_exercice": request.type_exercice,
        "difficulte": request.difficulte,
        "duree_estimee": 5,  # minutes (valeur par défaut)
        "points": 2.0,  # points de barème (valeur par défaut)
        "domaine": curriculum_service.get_domaine_by_chapitre(request.niveau, request.chapitre),
        "has_figure": spec.figure_geometrique is not None
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
