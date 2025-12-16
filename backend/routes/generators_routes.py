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
    generator_key: str = Field(description="Clé du générateur (ex: THALES_V1)")
    enonce_template_html: str = Field(description="Template HTML de l'énoncé")
    solution_template_html: str = Field(description="Template HTML de la solution")
    difficulty: str = Field(default="moyen")
    seed: Optional[int] = Field(default=None)
    svg_mode: str = Field(default="AUTO")


class DynamicPreviewResponse(BaseModel):
    success: bool
    enonce_html: str
    solution_html: str
    variables_used: Dict[str, Any]
    svg_enonce: Optional[str]
    svg_solution: Optional[str]
    errors: List[str] = Field(default_factory=list)


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/generators/{generator_key}/schema", response_model=GeneratorSchemaResponse, tags=["Generators"])
async def get_generator_schema_endpoint(generator_key: str):
    """Récupère le schéma complet d'un générateur dynamique."""
    schema = get_generator_schema(generator_key.upper())
    
    if not schema:
        available = get_all_generator_keys()
        raise HTTPException(
            status_code=404,
            detail={"error": "generator_not_found", "message": f"Générateur '{generator_key}' non trouvé", "available_generators": available}
        )
    
    return GeneratorSchemaResponse(**schema.to_dict())


@router.get("/generators/list", tags=["Generators"])
async def list_generators_endpoint():
    """Liste tous les générateurs disponibles."""
    summaries = get_all_schemas_summary()
    return {"generators": summaries, "count": len(summaries)}


@router.post("/preview-dynamic", response_model=DynamicPreviewResponse, tags=["Generators"])
async def preview_dynamic_exercise(request: DynamicPreviewRequest):
    """Prévisualise un exercice dynamique AVANT de le sauvegarder."""
    import re
    
    logger.info(f"🔍 Preview dynamic: generator={request.generator_key}, seed={request.seed}")
    
    errors = []
    
    schema = get_generator_schema(request.generator_key.upper())
    if not schema:
        raise HTTPException(status_code=400, detail={"error": "invalid_generator", "message": f"Générateur '{request.generator_key}' non reconnu"})
    
    try:
        gen_result = generate_dynamic_exercise(
            generator_key=request.generator_key.upper(),
            seed=request.seed,
            difficulty=request.difficulty
        )
        
        variables = gen_result.get("variables", {})
        results = gen_result.get("results", {})
        all_vars = {**variables, **results}
        
        enonce_html = render_template(request.enonce_template_html, all_vars)
        solution_html = render_template(request.solution_template_html, all_vars)
        
        unreplaced_enonce = re.findall(r'\{\{(\w+)\}\}', enonce_html)
        unreplaced_solution = re.findall(r'\{\{(\w+)\}\}', solution_html)
        
        for var in set(unreplaced_enonce + unreplaced_solution):
            errors.append(f"Variable inconnue: {{{{{var}}}}}")
        
        svg_enonce = gen_result.get("figure_svg_enonce") if request.svg_mode == "AUTO" else None
        svg_solution = gen_result.get("figure_svg_solution") if request.svg_mode == "AUTO" else None
        
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
        raise HTTPException(status_code=500, detail={"error": "preview_failed", "message": str(e)})


@router.post("/validate-template", tags=["Generators"])
async def validate_template(template: str, generator_key: str):
    """Valide les variables d'un template."""
    import re
    
    schema = get_generator_schema(generator_key.upper())
    if not schema:
        raise HTTPException(status_code=400, detail={"error": "invalid_generator"})
    
    used_vars = set(re.findall(r'\{\{(\w+)\}\}', template))
    known_var_names = {v.name for v in schema.variables}
    
    known = list(used_vars & known_var_names)
    unknown = list(used_vars - known_var_names)
    
    return {"valid": len(unknown) == 0, "unknown_variables": unknown, "known_variables": known}
