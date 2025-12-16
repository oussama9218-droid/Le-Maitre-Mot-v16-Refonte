"""
Routes API pour les générateurs dynamiques
==========================================

Endpoints:
- GET /api/v1/exercises/generators/{key}/schema : Schéma d'un générateur
- POST /api/admin/exercises/preview-dynamic : Preview d'un exercice dynamique

Version: 1.0.0 (P0.2 + P2)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from generators.generator_registry import (
    get_generator_schema,
    get_all_generator_keys,
    get_all_schemas_summary
)
from generators.thales_generator import generate_dynamic_exercise
from services.template_renderer import render_template
from logger import get_logger

logger = get_logger()

router = APIRouter()


# =============================================================================
# MODÈLES PYDANTIC
# =============================================================================

class GeneratorSchemaResponse(BaseModel):
    """Réponse pour le schéma d'un générateur."""
    generator_key: str
    label: str
    description: str
    niveau: str
    variables: List[Dict[str, Any]]
    svg_modes: List[str]
    supports_double_svg: bool
    difficulties: List[str]
    pedagogical_tips: Optional[str]
    template_example_enonce: str
    template_example_solution: str


class DynamicPreviewRequest(BaseModel):
    """Request pour prévisualiser un exercice dynamique."""
    generator_key: str = Field(description="Clé du générateur (ex: THALES_V1)")
    enonce_template_html: str = Field(description="Template HTML de l'énoncé avec {{variables}}")
    solution_template_html: str = Field(description="Template HTML de la solution avec {{variables}}")
    difficulty: str = Field(default="moyen", description="Difficulté pour le générateur")
    seed: Optional[int] = Field(default=None, description="Seed pour reproductibilité")
    svg_mode: str = Field(default="AUTO", description="Mode SVG: AUTO ou CUSTOM")


class DynamicPreviewResponse(BaseModel):
    """Réponse de prévisualisation d'un exercice dynamique."""
    success: bool
    enonce_html: str = Field(description="Énoncé rendu avec les variables injectées")
    solution_html: str = Field(description="Solution rendue avec les variables injectées")
    variables_used: Dict[str, Any] = Field(description="Variables générées et utilisées")
    svg_enonce: Optional[str] = Field(description="SVG de l'énoncé (si AUTO)")
    svg_solution: Optional[str] = Field(description="SVG de la solution (si AUTO)")
    errors: List[str] = Field(default_factory=list, description="Erreurs de rendu (variables inconnues, etc.)")


class GeneratorListResponse(BaseModel):
    """Réponse pour la liste des générateurs."""
    generators: List[Dict[str, Any]]
    count: int


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get(
    "/generators/{generator_key}/schema",
    response_model=GeneratorSchemaResponse,
    tags=["Generators"],
    summary="Récupère le schéma d'un générateur"
)
async def get_generator_schema_endpoint(generator_key: str):
    """
    Récupère le schéma complet d'un générateur dynamique.
    
    **Utilisé par l'admin** pour:
    - Afficher les variables disponibles et leurs types
    - Pré-remplir les templates avec des exemples
    - Indiquer les conseils pédagogiques
    
    **Exemple de réponse:**
    ```json
    {
        "generator_key": "THALES_V1",
        "label": "Agrandissements/Réductions",
        "variables": [
            {"name": "coefficient", "type": "number", "example": 2},
            {"name": "figure_type", "type": "string", "example": "triangle"}
        ],
        "svg_modes": ["AUTO", "CUSTOM"],
        "template_example_enonce": "..."
    }
    ```
    """
    schema = get_generator_schema(generator_key.upper())
    
    if not schema:
        available = get_all_generator_keys()
        raise HTTPException(
            status_code=404,
            detail={
                "error": "generator_not_found",
                "message": f"Générateur '{generator_key}' non trouvé",
                "available_generators": available
            }
        )
    
    return GeneratorSchemaResponse(**schema.to_dict())


@router.get(
    "/generators/list",
    response_model=GeneratorListResponse,
    tags=["Generators"],
    summary="Liste tous les générateurs disponibles"
)
async def list_generators_endpoint():
    """
    Liste tous les générateurs dynamiques disponibles avec un résumé.
    
    **Utilisé par l'admin** pour:
    - Afficher le dropdown de sélection du générateur
    - Montrer un aperçu rapide des capacités de chaque générateur
    """
    summaries = get_all_schemas_summary()
    return GeneratorListResponse(
        generators=summaries,
        count=len(summaries)
    )


@router.post(
    "/preview-dynamic",
    response_model=DynamicPreviewResponse,
    tags=["Generators"],
    summary="Prévisualise un exercice dynamique"
)
async def preview_dynamic_exercise(request: DynamicPreviewRequest):
    """
    Prévisualise un exercice dynamique AVANT de le sauvegarder.
    
    **Workflow:**
    1. Appelle le générateur avec seed optionnelle
    2. Injecte les variables dans les templates
    3. Retourne le HTML rendu + SVG + variables utilisées
    
    **Utilisé par l'admin** pour:
    - Tester que les templates sont corrects
    - Visualiser le rendu final avant sauvegarde
    - Identifier les erreurs de variables ({{var_inconnue}})
    
    **Gestion des erreurs:**
    - Si une variable {{xyz}} n'existe pas, elle apparaît dans "errors"
    - Le rendu continue avec la variable non remplacée
    """
    logger.info(f"🔍 Preview dynamic: generator={request.generator_key}, seed={request.seed}")
    
    errors = []
    
    # Vérifier que le générateur existe
    schema = get_generator_schema(request.generator_key.upper())
    if not schema:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_generator",
                "message": f"Générateur '{request.generator_key}' non reconnu",
                "available": get_all_generator_keys()
            }
        )
    
    try:
        # Générer les variables
        gen_result = generate_dynamic_exercise(
            generator_key=request.generator_key.upper(),
            seed=request.seed,
            difficulty=request.difficulty
        )
        
        variables = gen_result.get("variables", {})
        results = gen_result.get("results", {})
        
        # Fusionner variables et résultats pour le rendu
        all_vars = {**variables, **results}
        
        # Rendre les templates
        enonce_html = render_template(request.enonce_template_html, all_vars)
        solution_html = render_template(request.solution_template_html, all_vars)
        
        # Détecter les variables non remplacées (erreurs)
        import re
        unreplaced_enonce = re.findall(r'\{\{(\w+)\}\}', enonce_html)
        unreplaced_solution = re.findall(r'\{\{(\w+)\}\}', solution_html)
        
        for var in set(unreplaced_enonce + unreplaced_solution):
            errors.append(f"Variable inconnue: {{{{{var}}}}} - vérifiez l'orthographe")
        
        # SVG (mode AUTO)
        svg_enonce = None
        svg_solution = None
        
        if request.svg_mode == "AUTO":
            svg_enonce = gen_result.get("figure_svg_enonce")
            svg_solution = gen_result.get("figure_svg_solution")
        
        logger.info(f"✅ Preview generated: {len(all_vars)} variables, {len(errors)} errors")
        
        return DynamicPreviewResponse(
            success=len(errors) == 0,
            enonce_html=enonce_html,
            solution_html=solution_html,
            variables_used=all_vars,
            svg_enonce=svg_enonce,
            svg_solution=svg_solution,
            errors=errors
        )
        
    except Exception as e:
        logger.error(f"❌ Preview error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "preview_failed",
                "message": str(e)
            }
        )


# =============================================================================
# ENDPOINT VALIDATION DES TEMPLATES
# =============================================================================

class ValidateTemplateRequest(BaseModel):
    """Request pour valider un template."""
    template: str = Field(description="Template HTML avec {{variables}}")
    generator_key: str = Field(description="Clé du générateur")


class ValidateTemplateResponse(BaseModel):
    """Réponse de validation du template."""
    valid: bool
    unknown_variables: List[str] = Field(default_factory=list)
    known_variables: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


@router.post(
    "/validate-template",
    response_model=ValidateTemplateResponse,
    tags=["Generators"],
    summary="Valide les variables d'un template"
)
async def validate_template(request: ValidateTemplateRequest):
    """
    Valide un template SANS générer de preview complet.
    
    **Rapide et léger** - utilisé pour la validation en temps réel dans l'admin.
    
    Retourne:
    - unknown_variables: Variables utilisées mais non définies par le générateur
    - known_variables: Variables correctement reconnues
    - warnings: Suggestions et conseils
    """
    import re
    
    schema = get_generator_schema(request.generator_key.upper())
    if not schema:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_generator", "message": f"Générateur '{request.generator_key}' non reconnu"}
        )
    
    # Extraire les variables du template
    used_vars = set(re.findall(r'\{\{(\w+)\}\}', request.template))
    
    # Variables connues du générateur
    known_var_names = {v.name for v in schema.variables}
    
    known = list(used_vars & known_var_names)
    unknown = list(used_vars - known_var_names)
    
    warnings = []
    if unknown:
        warnings.append(f"Variables inconnues: {', '.join(unknown)}. Vérifiez l'orthographe ou consultez le schéma du générateur.")
    
    if not used_vars:
        warnings.append("Aucune variable {{...}} détectée dans le template. Est-ce volontaire ?")
    
    return ValidateTemplateResponse(
        valid=len(unknown) == 0,
        unknown_variables=unknown,
        known_variables=known,
        warnings=warnings
    )
